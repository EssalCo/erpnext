# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf8')

def execute():
    payment_details = "/private/files/payment_details.csv"
    payment = "/private/files/payment.csv"
    owners = "/private/files/owners.csv"
    parent_account = "50101 - حسابات الدائنون - N"
    print("Starting owners..")
    current_file = get_file_path(owners)
    company = frappe.get_doc(
        "Company",
        dict(
            company_name="Nahdi"
        )
    )
    main_cost_center = frappe.get_value(
        "Cost Center",
        dict(
            company=company.name,
            parent_cost_center=None
        ),
        "name"
    )

    cash_account = "3030601 - نقد - N"
    # with open(current_file, 'rb') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
    #     for row in spamreader:
    #         # print row
    #         try:
    #             serial_no = int(row[0])
    #         except:
    #             continue
    #         name = str(row[1])
    #
    #         doc = frappe.get_doc(
    #             dict(
    #                 doctype="Account",
    #                 account_name="{0} - {1}".format(serial_no, name),
    #                 account_number=None,
    #                 company=company.name,
    #                 is_group=0,
    #                 # account_currency="SAR",
    #                 parent_account=parent_account,
    #                 report_type="Balance Sheet"
    #             )
    #         )
    #         doc.flags.ignore_mandatory = True
    #         doc.insert(ignore_permissions=True)
    #
    # print("Done owners..")
    frappe.db.commit()
    print("Start Payments..")
    current_file = get_file_path(payment)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            # print row
            try:
                serial_no = int(row[0])
            except:
                continue

            post_date = row[1]
            post_date = datetime.strptime(
                str(post_date), '%Y/%m/%d'
            )
            account_no = str(row[2])
            value_1 = float(row[3])
            value_2 = float(row[4])
            value_3 = float(row[5])
            value_4 = float(row[6])
            cheq = str(row[7])
            bank = str(row[8])
            remark = str(row[9])
            pay_name = str(row[10])
            receipt_no = str(row[11])
            total = value_1 + value_2 + value_3 + value_4
            remark_str = ""
            if cheq:
                remark_str = remark_str + "CHEQNO: {0}".format(cheq)
            if bank:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "BANK: {0}".format(bank)
            if remark:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "REMARK: {0}".format(remark)
            if pay_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "PAY_NAME: {0}".format(pay_name)
            if receipt_no:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "RCP_NO: {0}".format(receipt_no)

            account_name = frappe.get_value(
                "Account",
                dict(
                    parent=parent_account,
                    name=("like", "{0} -%".format(account_no))
                )
            )
            print account_name
            journal_entry = frappe.get_doc(
                dict(
                    doctype="Journal Entry",
                    title=str(serial_no),
                    voucher_type="Journal Entry",
                    naming_series="JV-",
                    posting_date=post_date,
                    company=company.name,
                    user_remark=remark,
                    multi_currency=0,
                    remark=remark_str,
                    bill_date=datetime.now(),
                    third_party_creation=post_date,
                    accounts=[],
                    is_opening="No",
                    cheque_no=cheq
                )
            )

            journal_entry.append("accounts", dict(
                account=cash_account,
                against_account=account_name,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=abs(total),
                debit=abs(total),
                journal_note=remark,
                credit_in_account_currency=abs(0),
                credit=abs(0),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.append("accounts", dict(
                party_type="Company",
                party=company.name,
                account=account_name,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=0,
                debit=0,
                journal_note=remark,
                credit_in_account_currency=abs(total),
                credit=abs(total),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.flags.ignore_permissions = True

            journal_entry.submit()

            print journal_entry.name

    print("Done payment..")
    frappe.db.commit()

    print("Start Payments details..")
    current_file = get_file_path(payment_details)
    counter = 1
    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            # print row
            if row[0]:
                try:
                    serial_no = int(row[0])
                except:
                    continue
            else:
                pass
            if not serial_no:
                continue
            serial_no = "{:05d}".format(counter)
            counter += 1
            post_date = row[1]
            post_date = datetime.strptime(
                str(post_date), '%Y/%m/%d'
            )
            total = float(row[2])

            account_no = str(row[3])
            pay_no = str(row[4])
            serialno = str(row[5])
            remark = str(row[6])
            moa_no_name = str(row[7])
            pay_name = str(row[8])
            akar_no = str(row[9])
            akar_address = str(row[10])

            remark_str = ""
            if pay_no:
                remark_str = remark_str + "PAY_NO: {0}".format(pay_no)
            if serialno:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "SerialNo: {0}".format(serialno)
            if remark:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "REMARK: {0}".format(remark)
            if moa_no_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "MoaNoName: {0}".format(moa_no_name)
            if pay_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "PAY_NAME: {0}".format(pay_name)
            if akar_no:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "AKAR_NO: {0}".format(akar_no)
            if akar_address:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "AKAR_ADDRESS: {0}".format(akar_address)

            account_name = frappe.get_value(
                "Account",
                dict(
                    parent=parent_account,
                    name=("like", "{0} -%".format(account_no))
                )
            )
            journal_entry = frappe.get_doc(
                dict(
                    doctype="Journal Entry",
                    title=str(serial_no),
                    voucher_type="Journal Entry",
                    naming_series="JV-",
                    posting_date=post_date,
                    company=company.name,
                    user_remark=remark,
                    multi_currency=0,
                    remark=remark_str,
                    bill_date=datetime.now(),
                    third_party_creation=post_date,
                    accounts=[],
                    is_opening="No"
                )
            )

            journal_entry.append("accounts", dict(
                account=cash_account,
                against_account=account_name,
                party_type=None,
                party=None,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=abs(total),
                debit=abs(total),
                journal_note=remark,
                credit_in_account_currency=abs(0),
                credit=abs(0),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.append("accounts", dict(
                account=account_name,
                party_type="Company",
                party=company.name,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=0,
                debit=0,
                journal_note=remark,
                credit_in_account_currency=abs(total),
                credit=abs(total),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.flags.ignore_permissions = True

            journal_entry.submit()

            print journal_entry.name
    print("Done payment details..")
    frappe.db.commit()
