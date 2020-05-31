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


def execute_again():
    payment_details = "/private/files/nawat2019.csv"

    print("Starting journals..")

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="نواة للاستثمار العقاري"
        )
    )
    doc = frappe.get_doc(
        dict(
            doctype="Cost Center",
            cost_center_name="رئيسي",
            parent_cost_center=None,
            company=company.name,
            is_group=1
        )
    )
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)

    main_cost_center = doc.name

    current_file = get_file_path(payment_details)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        current_entry_index, total_credit, total_debit = 0, 0, 0
        journal_entry = None
        for row in spamreader:
            # print row
            try:
                account_serial_no = int(row[0])
            except:
                continue
            serial_no = int(row[2])
            pay_date = row[5]
            post_date = datetime.strptime(
                str(pay_date), '%Y/%m/%d'
            )
            if serial_no == 1:
                is_opening = "Yes"
            else:
                is_opening = "No"

            if serial_no != current_entry_index:
                if journal_entry:
                    journal_entry.total_debit = abs(total_debit)
                    journal_entry.total_credit = abs(total_credit)
                    journal_entry.difference = abs(total_debit - total_credit)
                    journal_entry.insert(ignore_permissions=True)
                    journal_entry.flags.ignore_permissions = True

                    journal_entry.submit()
                    total_credit, total_debit = 0, 0
                    print "submitted: ", journal_entry.name

                journal_entry = frappe.get_doc(
                    dict(
                        doctype="Journal Entry",
                        title="{1} القيد رقم ({0}) سنة".format(serial_no, 2019),
                        voucher_type="Journal Entry",
                        naming_series="JV-",
                        posting_date=post_date,
                        company=company.name,
                        user_remark="{1} القيد رقم ({0}) سنة".format(serial_no, 2019),
                        multi_currency=0,
                        remark="{1} القيد رقم ({0}) سنة".format(serial_no, 2019),
                        bill_date=datetime.now(),
                        third_party_creation=post_date,
                        accounts=[],
                        is_opening=is_opening
                    )
                )
                current_entry_index = serial_no

            remark = str(row[6])
            debit = float(row[7].replace(",", ""))
            credit = float(row[8].replace(",", ""))

            if credit:
                total_credit += credit
            else:
                total_debit += debit

            account_name = frappe.get_value(
                "Account",
                dict(
                    account_serial=account_serial_no,
                    company=company.name
                ),
                "name"
            )
            journal_entry.append("accounts", dict(
                account=account_name,
                party_type=None,
                party=None,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=abs(debit),
                debit=abs(debit),
                journal_note=remark,
                credit_in_account_currency=abs(credit),
                credit=abs(credit),
                is_advance="No",
                cost_center=main_cost_center
            ))
            frappe.db.commit()
    if journal_entry:
        journal_entry.total_debit = abs(total_debit)
        journal_entry.total_credit = abs(total_credit)
        journal_entry.difference = abs(total_debit - total_credit)
        journal_entry.insert(ignore_permissions=True)
        journal_entry.flags.ignore_permissions = True

        journal_entry.submit()

        print journal_entry.name
    print("Done Journals.")


    frappe.db.commit()