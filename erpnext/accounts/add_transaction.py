# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback
from datetime import datetime

import frappe
from erpnext.utilities.send_telegram import send_msg_telegram
# from erpnext.accounts.general_ledger import make_gl_entries
from frappe.utils import flt
import json


@frappe.whitelist(allow_guest=True)
def add_transaction():
    # 'from_account',
    # 'to_account',
    # 'credit_amount',
    # 'debit_amount',
    # 'statement',
    # ‘company’
    # ‘branch’
    # ‘user_id’
    # ‘customer_id’
    # ‘contract_id’
    # `vat_amount`
    # `vat_account`
    # `cost_center`
    # `date`
    # `third_party_creation`
    try:

        data = frappe.form_dict
        from_account = data.get('from_account')
        to_account = data.get('to_account')
        credit_amount = float(data.get('credit_amount', 0))
        debit_amount = float(data.get('debit_amount', 0))
        statement = data.get('statement')
        # operation = frappe.form_dict['operation']
        contract_id = data.get('contract_id')
        # payment_id = frappe.form_dict['payment_id']
        # property_id = frappe.form_dict['property_id']
        # unit_id = frappe.form_dict['unit_id']
        user_id = data.get('user_id')
        customer_id = data.get('customer_id')
        customer_name = data.get('customer_name')
        # transaction_id = frappe.form_dict['transaction_id']
        company_id = data.get('company')
        branch_id = data.get('branch')
        vat_amount = float(data.get('vat_amount', 0))
        vat_account = data.get('vat_account')
        cost_center = data.get('cost_center')
        third_party_creation = data.get('third_party_creation')
        date = data.get('date', datetime.now())

        frappe.set_user("Administrator")

        if branch_id:
            company_id = branch_id

        # if vat_amount and not vat_account:
        #     return dict(status=False, message="You must specify Vat Account since there is a vat")
        # if not credit_amount and not debit_amount:
        #     return dict(status=False, message="Debit and credit cannot be both zero")
        # if from_account == to_account:
        #     return dict(status=False, message="You cannot transfer within the same account")

        if len(frappe.get_list("Customer", filters={"customer_name": ("LIKE", "%@{0}".format(customer_id))})) == 0:
            customer_group = frappe.get_list("Customer Group",
                                             fields=["name"],
                                             ignore_permissions=True,
                                             limit=1)
            customer_group = customer_group[0]["name"] if len(customer_group) else "Individual"
            customer_territory = frappe.get_list("Territory",
                                                 fields=["name"],
                                                 ignore_permissions=True,
                                                 limit=1)
            customer_territory = customer_territory[0]["name"] if len(customer_territory) else "All Territories"

            to_customer = frappe.get_doc(
                doctype="Customer",
                naming_series="CUST-",
                customer_name="{0}@{1}".format(customer_name, customer_id),
                customer_type="Individual",
                customer_group=customer_group,
                territory=customer_territory,
                disabled=0,
                default_currency="SAR",
                language="ar"
            )
            to_customer.insert(ignore_permissions=True)
        else:
            to_customer = frappe.get_doc(
                "Customer",
                dict(
                    customer_name=("like", "%@{0}".format(customer_id))
                )
            )

        # if not frappe.db.exists(
        #         "Customer",
        #         dict(
        #             customer_name=user_id
        #         )
        # ):
        #     customer = frappe.get_doc(
        #         doctype="Customer",
        #         naming_series="CUST-",
        #         customer_name=user_id,
        #         customer_type="Company",
        #         customer_group="Commercial",
        #         territory="All Territories",
        #         disabled=0,
        #         default_currency="SAR",
        #         language="ar"
        #     )
        #     customer.insert(ignore_permissions=True)
        # else:
        #     customer = frappe.get_doc(
        #         "Customer",
        #         dict(
        #             customer_name=user_id
        #         )
        #     )
        # if credit_amount:
        #     customer, to_customer = to_customer, customer
        #     payment_type = "Receive"
        #     amount = credit_amount
        # elif debit_amount:
        #     payment_type = "Pay"
        #     amount = debit_amount

        journal_entry = frappe.get_doc(
            dict(
                doctype="Journal Entry",
                title=statement,
                voucher_type="Journal Entry",
                naming_series="JV-",
                posting_date=date,
                company=company_id,
                user_remark=statement,
                total_debit=abs(debit_amount),
                total_credit=abs(credit_amount),
                difference=abs(debit_amount - credit_amount),
                multi_currency=0,
                remark=statement,
                bill_no=contract_id,
                bill_date=datetime.now(),
                is_opening="No",
                third_party_creation=third_party_creation,
                accounts=[]
            )
        )
        project = frappe.get_value("Project", dict(), "name")
        if credit_amount:
            journal_entry.append("accounts", dict(
                account=from_account,
                party_type="Customer",
                party=to_customer.name,
                exchange_rate=1,
                debit_in_account_currency=abs(credit_amount),
                debit=abs(credit_amount),
                credit_in_account_currency=0,
                credit=0,
                project=project,
                is_advance="No",
                against_account=to_account,
                cost_center=cost_center
            ))
            journal_entry.append("accounts", dict(
                account=to_account,
                party_type="Company",
                party=company_id,
                exchange_rate=1,
                debit_in_account_currency=0,
                debit=0,
                credit_in_account_currency=abs(credit_amount) - abs(vat_amount),
                credit=abs(credit_amount) - abs(vat_amount),
                project=project,
                is_advance="No",
                against_account=from_account,
                cost_center=cost_center
            ))
            if vat_amount:
                journal_entry.append("accounts", dict(
                    account=vat_account,
                    party_type="Company",
                    party=company_id,
                    exchange_rate=1,
                    debit_in_account_currency=0,
                    debit=0,
                    credit_in_account_currency=abs(vat_amount),
                    credit=abs(vat_amount),
                    project=project,
                    is_advance="No",
                    against_account=from_account,
                    cost_center=cost_center
                ))
        else:
            journal_entry.append("accounts", dict(
                account=from_account,
                party_type="Customer",
                party=to_customer.name,
                exchange_rate=1,
                debit_in_account_currency=abs(credit_amount),
                debit=abs(credit_amount),
                credit_in_account_currency=0,
                credit=0,
                project=project,
                is_advance="No",
                against_account=to_account,
                cost_center=cost_center
            ))
            journal_entry.append("accounts", dict(
                account=to_account,
                party_type="Company",
                party=company_id,
                exchange_rate=1,
                debit_in_account_currency=abs(credit_amount) - abs(vat_amount),
                debit=abs(credit_amount) - abs(vat_amount),
                credit_in_account_currency=0,
                credit=0,
                project=project,
                is_advance="No",
                against_account=from_account,
                cost_center=cost_center
            ))
            if vat_amount:
                journal_entry.append("accounts", dict(
                    account=vat_account,
                    party_type="Company",
                    party=company_id,
                    exchange_rate=1,
                    debit_in_account_currency=abs(vat_amount),
                    debit=abs(vat_amount),
                    credit_in_account_currency=0,
                    credit=0,
                    project=project,
                    is_advance="No",
                    against_account=from_account,
                    cost_center=cost_center
                ))
        journal_entry.insert(ignore_permissions=True)
        # payment_entry = frappe.get_doc(
        #     dict(
        #         doctype="Payment Entry",
        #         naming_series="PE-",
        #         payment_type=payment_type,
        #         posting_date=datetime.now().date(),
        #         company=company_id,
        #         mode_of_payment="Cash",
        #         party_type="Customer",
        #         party=to_customer.name,
        #         party_name=to_customer.customer_name,
        #         paid_from=from_account,
        #         paid_from_account_currency="SAR",
        #         paid_to=to_account,
        #         paid_to_account_currency="SAR",
        #         paid_amount=abs(amount),
        #         source_exchange_rate=1,
        #         base_paid_amount=abs(amount),
        #         received_amount=0,
        #         target_exchange_rate=1,
        #         base_received_amount=0,
        #         reference_no="{0} - {1}".format(contract_id, statement),
        #         reference_date=datetime.now().date()
        #     )
        # )
        # payment_entry.insert(ignore_permissions=True)

        # gl_entries = get_gl_entries(payment_entry=payment_entry)

        # if gl_entries:
        #     # if POS and amount is written off, updating outstanding amt after posting all gl entries
        #     update_outstanding = "Yes"
        #     make_gl_entries(
        #         gl_entries,
        #         cancel=False,
        #         update_outstanding=update_outstanding,
        #         merge_entries=False)
        frappe.db.commit()
    except Exception as e:
        error_msg = "Error : " + traceback.format_exc()
        send_msg_telegram(error_msg)
        return dict(status=False, message=str(e))
    return dict(status=True, message="Transactions are added to erpnext successfully")


def get_gl_entries(payment_entry):
    # from erpnext.accounts.general_ledger import merge_similar_entries
    gl_entries = []

    make_transaction(gl_entries, payment_entry)

    # make_sales_gl_entry(gl_entries)
    #
    # make_purchase_gl_entries(gl_entries)

    # self.add_extra_loss_or_benifit(gl_entries)
    # gl_entries = merge_similar_entries(gl_entries)

    return gl_entries


def make_sales_gl_entry(gl_entries):
    pass


def make_purchase_gl_entries(gl_entries):
    pass


def make_transaction(gl_entries, payment_entry):
    cash_grand_total = flt(payment_entry.paid_amount, payment_entry.precision("paid_amount"))

    if cash_grand_total:
        payment_entry.remarks = payment_entry.reference_no

        gl_entries.append(
            get_gl_dict({
                "account": payment_entry.paid_from,
                "party_type": payment_entry.party_type,
                "party": payment_entry.party,
                "against": payment_entry.paid_to,
                "credit": cash_grand_total,
                "credit_in_account_currency": cash_grand_total,
                "against_voucher": payment_entry.name,
                "against_voucher_type": payment_entry.doctype
            }, payment_entry)
        )
        payment_entry.remarks = payment_entry.reference_no

        gl_entries.append(
            get_gl_dict({
                "account": payment_entry.paid_to,
                "party_type": payment_entry.party_type,
                "party": payment_entry.party,
                "against": payment_entry.paid_from,
                "debit": cash_grand_total,
                "debit_in_account_currency": cash_grand_total,
                "against_voucher": payment_entry.name,
                "against_voucher_type": payment_entry.doctype
            }, payment_entry)
        )


def get_gl_dict(data, payment_entry):
    """this method populates the common properties of a gl entry record"""

    fiscal_year = str(datetime.now().year)

    gl_dict = frappe._dict({
        'company': payment_entry.company,
        'posting_date': payment_entry.posting_date,
        'fiscal_year': fiscal_year,
        'voucher_type': payment_entry.doctype,
        'voucher_no': payment_entry.name,
        'remarks': payment_entry.get("remarks"),
        'debit': 0,
        'credit': 0,
        'debit_in_account_currency': 0,
        'credit_in_account_currency': 0,
        'is_opening': payment_entry.get("is_opening") or "No",
        'party_type': None,
        'party': None,
        'project': frappe.get_value("Project", dict(), "name")
    })
    gl_dict.update(data)

    return gl_dict


@frappe.whitelist(allow_guest=True)
def add_transaction_v2():
    # 'contract_id',
    # 'date',
    # 'transactions_list',
    # 'company',
    # 'branch',
    # 'user_id'
    # 'statement'
    # 'third_party_creation'

    try:

        data = frappe.form_dict
        contract_id = data.get('contract_id')
        date = data.get('date')
        transactions_list = data.get('transactions_list', '[]')
        company = data.get('company')
        branch = frappe.form_dict.get('branch')
        user_id = data.get('user_id')
        statement = data.get('statement', '')
        third_party_creation = data.get('third_party_creation', datetime.now())

        frappe.set_user("Administrator")

        if branch:
            company = branch

        journal_entry = frappe.get_doc(
            dict(
                doctype="Journal Entry",
                title=statement,
                voucher_type="Journal Entry",
                naming_series="JV-",
                posting_date=date,
                company=company,
                user_remark=statement,
                multi_currency=0,
                remark=statement,
                bill_no=contract_id,
                bill_date=datetime.now(),
                is_opening="No",
                third_party_creation=third_party_creation,
                accounts=[]
            )
        )
        project = frappe.get_value("Project", dict(), "name")
        total_credit = total_debit = 0
        import json
        transactions_list = json.loads(transactions_list)
        send_msg_telegram("transactions" + str(transactions_list))

        for transaction in transactions_list:
            debit = float(transaction.get('debit_amount', 0) or 0)
            credit = float(transaction.get('credit_amount', 0) or 0)
            _statement = transaction('statement', '')
            cost_center = transaction.get('cost_center')
            account = transaction.get('account')
            vat_amount = transaction.get('vat_amount', 0)
            vat_account = transaction.get('vat_account', 0)
            if credit:
                total_credit += credit
                journal_entry.append("accounts", dict(
                    account=account,
                    exchange_rate=1,
                    debit_in_account_currency=abs(credit),
                    debit=abs(credit),
                    journal_note=_statement,
                    credit_in_account_currency=0,
                    credit=0,
                    project=project,
                    is_advance="No",
                    cost_center=cost_center
                ))
                journal_entry.append("accounts", dict(
                    account=account,
                    party_type="Company",
                    party=company,
                    exchange_rate=1,
                    debit_in_account_currency=0,
                    debit=0,
                    journal_note=_statement,
                    credit_in_account_currency=abs(credit) - abs(vat_amount),
                    credit=abs(credit) - abs(vat_amount),
                    project=project,
                    is_advance="No",
                    cost_center=cost_center
                ))
                if vat_amount and vat_account:
                    journal_entry.append("accounts", dict(
                        account=vat_account,
                        party_type="Company",
                        party=company,
                        exchange_rate=1,
                        debit_in_account_currency=0,
                        debit=0,
                        credit_in_account_currency=abs(vat_amount),
                        credit=abs(vat_amount),
                        project=project,
                        is_advance="No",
                        cost_center=cost_center
                    ))
            else:
                total_debit += debit
                journal_entry.append("accounts", dict(
                    account=account,
                    exchange_rate=1,
                    debit_in_account_currency=abs(debit),
                    debit=abs(debit),
                    credit_in_account_currency=0,
                    credit=0,
                    project=project,
                    journal_note=_statement,
                    is_advance="No",
                    cost_center=cost_center
                ))
                journal_entry.append("accounts", dict(
                    account=account,
                    party_type="Company",
                    party=company,
                    exchange_rate=1,
                    debit_in_account_currency=abs(debit) - abs(vat_amount),
                    debit=abs(debit) - abs(vat_amount),
                    credit_in_account_currency=0,
                    credit=0,
                    project=project,
                    is_advance="No",
                    journal_note=_statement,
                    cost_center=cost_center
                ))
                if vat_amount and vat_account:
                    journal_entry.append("accounts", dict(
                        account=vat_account,
                        party_type="Company",
                        party=company,
                        exchange_rate=1,
                        debit_in_account_currency=abs(vat_amount),
                        debit=abs(vat_amount),
                        credit_in_account_currency=0,
                        credit=0,
                        project=project,
                        is_advance="No",
                        cost_center=cost_center
                    ))
        journal_entry.total_debit = abs(total_debit),
        journal_entry.total_credit = abs(total_credit),
        journal_entry.difference = abs(total_debit - total_credit),
        journal_entry.insert(ignore_permissions=True)

        frappe.db.commit()
    except Exception as e:
        error_msg = "Error : " + traceback.format_exc()
        send_msg_telegram(error_msg)
        return dict(status=False, message=str(e))
    return dict(status=True, message="Transactions are added to erpnext successfully")
