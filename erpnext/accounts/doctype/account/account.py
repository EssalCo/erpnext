# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe
from frappe import throw, _
from frappe.utils import cint, cstr
from frappe.utils.nestedset import NestedSet
from erpnext.utilities.send_telegram import send_msg_telegram


class RootNotEditable(frappe.ValidationError): pass


class BalanceMismatchError(frappe.ValidationError): pass


class Account(NestedSet):
    nsm_parent_field = 'parent_account'

    def onload(self):
        frozen_accounts_modifier = frappe.db.get_value("Accounts Settings", "Accounts Settings",
                                                       "frozen_accounts_modifier")
        if not frozen_accounts_modifier or frozen_accounts_modifier in frappe.get_roles():
            self.set_onload("can_freeze_account", True)

    def autoname(self):
        self.name = get_account_autoname(self.account_number, self.account_name, self.company)
        self.get_account_serial()

    def before_insert(self):
        #send_msg_telegram("before insert " + str( self.account_serial) + str(self.account_serial_x))
        serial = self.account_name.split(" -")[0]
        if serial.isdigit():
            self.account_serial = serial
        else:
            self.get_account_serial()
            if self.account_serial and not serial.isdigit():
                self.account_name = "{0} - {1}".format(self.account_serial, self.account_name)
        #send_msg_telegram("after insert " + str( self.account_serial) + str(self.account_serial_x))


    def before_save(self):
        if not self.account_serial or self.parent_account != frappe.get_value("Account", self.name, "parent_account"):
            self.get_account_serial()

    def validate(self):

        if frappe.local.flags.allow_unverified_charts:
            return
        self.validate_parent()
        self.validate_root_details()
        validate_account_number(self.name, self.account_number, self.company)
        self.validate_group_or_ledger()
        self.set_root_and_report_type()
        self.validate_mandatory()
        self.validate_frozen_accounts_modifier()
        self.validate_balance_must_be_debit_or_credit()
        self.validate_account_currency()


    def validate_parent(self):
        """Fetch Parent Details and validate parent account"""
        if self.parent_account:
            par = frappe.db.get_value("Account", self.parent_account,
                                      ["name", "is_group", "company"], as_dict=1)
            if not par:
                throw(_("Account {0}: Parent account {1} does not exist").format(self.name, self.parent_account))
            elif par.name == self.name:
                throw(_("Account {0}: You can not assign itself as parent account").format(self.name))
            elif not par.is_group:
                throw(_("Account {0}: Parent account {1} can not be a ledger").format(self.name, self.parent_account))
            elif par.company != self.company:
                throw(_("Account {0}: Parent account {1} does not belong to company: {2}")
                      .format(self.name, self.parent_account, self.company))

    def set_root_and_report_type(self):
        if self.parent_account:
            par = frappe.db.get_value("Account", self.parent_account,
                                      ["report_type", "root_type"], as_dict=1)

            if par.report_type:
                self.report_type = par.report_type
            if par.root_type:
                self.root_type = par.root_type

        if self.is_group:
            db_value = frappe.db.get_value("Account", self.name, ["report_type", "root_type"], as_dict=1)
            if db_value:
                if self.report_type != db_value.report_type:
                    frappe.db.sql("update `tabAccount` set report_type=%s where lft > %s and rgt < %s",
                                  (self.report_type, self.lft, self.rgt))
                if self.root_type != db_value.root_type:
                    frappe.db.sql("update `tabAccount` set root_type=%s where lft > %s and rgt < %s",
                                  (self.root_type, self.lft, self.rgt))

        if self.root_type and not self.report_type:
            self.report_type = "Balance Sheet" \
                if self.root_type in ("Asset", "Liability", "Equity") else "Profit and Loss"

    def validate_root_details(self):
        # does not exists parent
        if frappe.db.exists("Account", self.name):
            if not frappe.db.get_value("Account", self.name, "parent_account"):
                throw(_("Root cannot be edited."), RootNotEditable)

        if not self.parent_account and not self.is_group:
            frappe.throw(_("Root Account must be a group"))

    def validate_group_or_ledger(self):
        if self.get("__islocal"):
            return

        existing_is_group = frappe.db.get_value("Account", self.name, "is_group")
        if cint(self.is_group) != cint(existing_is_group):
            if self.check_gle_exists():
                throw(_("Account with existing transaction cannot be converted to ledger"))
            elif self.is_group:
                if self.account_type and not self.flags.exclude_account_type_check:
                    throw(_("Cannot covert to Group because Account Type is selected."))
            elif self.check_if_child_exists():
                throw(_("Account with child nodes cannot be set as ledger"))

    def validate_frozen_accounts_modifier(self):
        old_value = frappe.db.get_value("Account", self.name, "freeze_account")
        if old_value and old_value != self.freeze_account:
            frozen_accounts_modifier = frappe.db.get_value('Accounts Settings', None, 'frozen_accounts_modifier')
            if not frozen_accounts_modifier or \
                            frozen_accounts_modifier not in frappe.get_roles():
                throw(_("You are not authorized to set Frozen value"))

    def validate_balance_must_be_debit_or_credit(self):
        from erpnext.accounts.utils import get_balance_on
        if not self.get("__islocal") and self.balance_must_be:
            account_balance = get_balance_on(self.name)

            if account_balance > 0 and self.balance_must_be == "Credit":
                frappe.throw(
                    _("Account balance already in Debit, you are not allowed to set 'Balance Must Be' as 'Credit'"))
            elif account_balance < 0 and self.balance_must_be == "Debit":
                frappe.throw(
                    _("Account balance already in Credit, you are not allowed to set 'Balance Must Be' as 'Debit'"))

    def validate_account_currency(self):
        if not self.account_currency:
            self.account_currency = frappe.db.get_value("Company", self.company, "default_currency")

        elif self.account_currency != frappe.db.get_value("Account", self.name, "account_currency"):
            if frappe.db.get_value("GL Entry", {"account": self.name}):
                frappe.throw(_("Currency can not be changed after making entries using some other currency"))

    def convert_group_to_ledger(self):
        if self.check_if_child_exists():
            throw(_("Account with child nodes cannot be converted to ledger"))
        elif self.check_gle_exists():
            throw(_("Account with existing transaction cannot be converted to ledger"))
        else:
            self.is_group = 0
            self.save()
            return 1

    def convert_ledger_to_group(self):
        if self.check_gle_exists():
            throw(_("Account with existing transaction can not be converted to group."))
        elif self.account_type and not self.flags.exclude_account_type_check:
            throw(_("Cannot covert to Group because Account Type is selected."))
        else:
            self.is_group = 1
            self.save()
            return 1

    # Check if any previous balance exists
    def check_gle_exists(self):
        return frappe.db.get_value("GL Entry", {"account": self.name})

    def check_if_child_exists(self):
        return frappe.db.sql("""select name from `tabAccount` where parent_account = %s
			and docstatus != 2""", self.name)

    def validate_mandatory(self):
        if not self.root_type:
            throw(_("Root Type is mandatory"))

        if not self.report_type:
            throw(_("Report Type is mandatory"))

    def on_trash(self):
        # checks gl entries and if child exists
        if self.check_gle_exists():
            throw(_("Account with existing transaction can not be deleted"))

        super(Account, self).on_trash(True)

    def get_account_serial(self):
        try:
            if getattr(self, "account_serial", None) and not getattr(self, "account_serial_x", None):
                self.account_serial_x = str(self.account_serial)
                return
            # if not getattr(self, "account_serial_x", None):
            #     send_msg_telegram("return " + str(self.account_serial) + str(self.account_serial_x))
            #     return
            if not self.parent_account:
                #send_msg_telegram("no parent " + str(self.account_serial) + str(self.account_serial_x))

                last_existing_serial = frappe.db.sql("""SELECT 
        MAX(account_serial) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account IS NULL;""", (self.company,), as_dict=True)
                if len(last_existing_serial) == 0 or not last_existing_serial[0].maxi:
                    # last_existing_serial = 0
                    next_serial = 1
                    next_serial_str = "#1"
                else:
                    last_existing_serial = last_existing_serial[0].maxi
                    next_serial = last_existing_serial + 1
                    next_serial_str = "#{0}".format(last_existing_serial + 1)
            else:
                #send_msg_telegram("parent " + str(self.account_serial) + str(self.account_serial_x))

                last_existing_serial = frappe.db.sql("""SELECT account_serial, account_serial_x, name FROM
      `tabAccount` WHERE
       account_serial = (
    SELECT 
        MAX(account_serial * 1) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s);""", (self.company, self.parent_account), as_dict=True)
                parent_serial, account_serial_x = frappe.db.get_value(
                    "Account",
                    self.parent_account,
                    [
                    "account_serial",
                        "account_serial_x"
                        ]
                )
                if len(last_existing_serial) == 0 or not last_existing_serial[0].account_serial:
                    last_existing_serial = parent_serial * 100
                    next_serial = last_existing_serial + 1
                    next_serial_str = "{0}.{1}".format(parent_serial, 1)
                else:
                    last_existing_serial = last_existing_serial[0].account_serial
                    next_serial = last_existing_serial + 1

                    # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
                    next_serial_str = "{0}.{1}".format(account_serial_x, next_serial)
            #send_msg_telegram("finish " + str(self.account_serial) + str(self.account_serial_x))

            self.account_serial = next_serial
            self.account_serial_x = next_serial_str
        except:
            import traceback
            send_msg_telegram(traceback.format_exc() + "\n" + str(self.account_serial) + "\n" + str(self.account_serial_x))


def get_parent_account(doctype, txt, searchfield, start, page_len, filters):
    return frappe.db.sql("""select name from tabAccount
		where is_group = 1 and docstatus != 2 and company = %s
		and %s like %s order by name limit %s, %s""" %
                         ("%s", searchfield, "%s", "%s", "%s"),
                         (filters["company"], "%%%s%%" % txt, start, page_len), as_list=1)


def get_account_currency(account):
    """Helper function to get account currency"""
    if not account:
        return

    def generator():
        try:
            account_currency, company = frappe.db.get_value("Account", account, ["account_currency", "company"])
        except:
            throw(_("Account {0} does not exist! Please choose a valid account.").format(account))

        if not account_currency:
            account_currency = frappe.db.get_value("Company", company, "default_currency")

        return account_currency

    return frappe.local_cache("account_currency", account, generator)


def get_account_autoname(account_number, account_name, company):
    # first validate if company exists
    company = frappe.db.get_value("Company", company, ["abbr", "name"], as_dict=True)
    if not company:
        frappe.throw(_('Company {0} does not exist').format(company))

    parts = [account_name.strip(), company.abbr]
    if cstr(account_number).strip():
        parts.insert(0, cstr(account_number).strip())
    return ' - '.join(parts)


def validate_account_number(name, account_number, company):
    if account_number:
        account_with_same_number = frappe.db.get_value("Account",
                                                       {"account_number": account_number, "company": company,
                                                        "name": ["!=", name]})
        if account_with_same_number:
            frappe.throw(_("Account Number {0} already used in account {1}")
                         .format(account_number, account_with_same_number))


@frappe.whitelist()
def update_account_number(name, account_name, account_number=None):
    account = frappe.db.get_value("Account", name, "company", as_dict=True)
    if not account: return
    validate_account_number(name, account_number, account.company)
    if account_number:
        frappe.db.set_value("Account", name, "account_number", account_number.strip())
    else:
        frappe.db.set_value("Account", name, "account_number", "")
    frappe.db.set_value("Account", name, "account_name", account_name.strip())

    new_name = get_account_autoname(account_number, account_name, account.company)
    if name != new_name:
        frappe.rename_doc("Account", name, new_name, ignore_permissions=1)
        return new_name


@frappe.whitelist()
def merge_account(old, new, is_group, root_type, company):
    # Validate properties before merging
    if not frappe.db.exists("Account", new):
        throw(_("Account {0} does not exist").format(new))

    val = list(frappe.db.get_value("Account", new,
                                   ["is_group", "root_type", "company"]))

    if val != [cint(is_group), root_type, company]:
        throw(_(
            """Merging is only possible if following properties are same in both records. Is Group, Root Type, Company"""))

    if is_group and frappe.db.get_value("Account", new, "parent_account") == old:
        frappe.db.set_value("Account", new, "parent_account",
                            frappe.db.get_value("Account", old, "parent_account"))

    frappe.rename_doc("Account", old, new, merge=1, ignore_permissions=1)

    return new


def add_serial_to_existing_account_tree(company):
    parent_account = None

    first_orders_accounts = frappe.db.sql("""SELECT
    name
    FROM
    tabAccount 
    WHERE company = %s 
    AND parent_account IS NULL;""", (company,), as_dict=True)
