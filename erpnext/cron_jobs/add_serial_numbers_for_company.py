# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import frappe


def execute():
    companies = frappe.get_list(
        "Company",
        fields=["name"],
        filters=dict(
            name="AL Mather Trading EST"
        ),
        ignore_permissions=True
    )

    for _company in companies:
        company = _company.name
        frappe.db.sql(
            """UPDATE
            `tabAccount` SET `account_serial` = ''
            WHERE `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )
        accounts = frappe.db.sql(
            """SELECT `name`, `company` FROM 
            `tabAccount` WHERE (`parent_account` IS NULL OR `parent_account` = '') 
            AND `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )

        for acc in accounts:
            account = frappe.get_doc("Account", acc.name)
            last_existing_serial = frappe.db.sql("""SELECT 
        MAX(account_serial) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account IS NULL;""", (company,), as_dict=True)
            if len(last_existing_serial) == 0 or not last_existing_serial[0].maxi:
                # last_existing_serial = 0
                next_serial = 1
                next_serial_str = "#1"
            else:
                last_existing_serial = last_existing_serial[0].maxi
                next_serial = int(last_existing_serial or 0) + 1
                next_serial_str = "#{0}".format(next_serial)
            frappe.db.sql("""UPDATE `tabAccount` SET `account_serial` = '{0}',
                         `account_serial_x` = '{1}' WHERE `name` = '{2}';""".format(
                int(next_serial),
                next_serial_str,
                account.name
            ))
            frappe.db.commit()
            print "PARENT"
            print str(next_serial)
            print str(next_serial_str)
            update_children_serials(account.name)

        #######################
        accounts = frappe.db.sql(
            """SELECT `name`, `company`, `account_name`, `account_serial` FROM 
            `tabAccount` WHERE `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )

        for account in accounts:
            serial = account.account_name.split(" -")[0]
            if serial.isdigit():
                account.account_name = account.account_name.replace(account.account_name.split(" -")[0], "")[2:]
            frappe.db.set_value(
                "Account",
                account.name,
                "account_name",
                "{0} - {1}".format(account.account_serial, account.account_name)
            )

def update_children_serials(parent_account):
    accounts = frappe.db.sql(
        """SELECT `name` FROM 
        `tabAccount` WHERE  `parent_account` = %(parent)s ORDER BY `creation` ASC;""",
        dict(parent=parent_account), as_dict=True
    )

    if len(accounts) == 0:
        return
    for acc in accounts:
        account = frappe.get_doc("Account", acc.name)
        print("CHILD")
        # if not getattr(self, "account_serial_x", None):
        #     send_msg_telegram("return " + str(self.account_serial) + str(self.account_serial_x))
        #     return

        # send_msg_telegram("parent " + str(self.account_serial) + str(self.account_serial_x))

        last_existing_serial = frappe.db.sql("""SELECT account_serial, account_serial_x, name FROM
      `tabAccount` WHERE
       account_serial = (
    SELECT 
        MAX(account_serial * 1) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s);""", (account.company, account.parent_account), as_dict=True)
        parent_serial, account_serial_x = frappe.db.get_value(
            "Account",
            account.parent_account,
            [
                "account_serial",
                "account_serial_x"
            ]
        )
        # send_msg_telegram("parent acc " + str(parent_serial) + " " + str(account_serial_x))
        # send_msg_telegram("parent account " + str(last_existing_serial))

        if len(last_existing_serial) == 0 or not last_existing_serial[0].account_serial:
            print("NOT FOUND")
            print(parent_serial)
            print(last_existing_serial + 1)
            last_existing_serial = long(parent_serial) * 100
            # send_msg_telegram("sum " + str(last_existing_serial))
            next_serial = last_existing_serial + 1
            next_serial_str = "{0}.{1}".format(parent_serial, 1)
        else:
            print("FOUND")
            print(last_existing_serial[0].account_serial)
            last_existing_serial = long(last_existing_serial[0].account_serial)
            # send_msg_telegram("query " + str(last_existing_serial))

            next_serial = last_existing_serial + 1

            # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
            next_serial_str = "{0}.{1}".format(account_serial_x, next_serial)

            # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
            # next_serial_str = "{0}.{1}".format(parent_serial, int(trimmed_serial) + 1)
        # send_msg_telegram("finish " + str(self.account_serial) + str(self.account_serial_x))
        print(str(next_serial_str))
        print(str(next_serial))
        frappe.db.sql("""UPDATE `tabAccount` SET `account_serial` = '{0}', 
        `account_serial_x` = '{1}' WHERE `name` = '{2}';""".format(
            int(next_serial),
            next_serial_str,
            account.name
        ))
        frappe.db.commit()

        update_children_serials(account.name)
    # self.account_serial = int(next_serial_str.replace(".", "").replace("#", ""))
    # self.account_serial_x = next_serial_str
    # except Exception as e:
    #     print str(e)
    # account.get_account_serial()
    # account.save(ignore_permissions=True)
