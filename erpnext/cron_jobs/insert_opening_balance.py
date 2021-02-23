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
    payment_details = "/private/files/kintal_ops.csv"

    print("Starting journals..")

    company = frappe.get_doc(
        "Company",
        dict(
            abbr="KA"
        )
    )
    # doc = frappe.get_doc(
    #     dict(
    #         doctype="Cost Center",
    #         cost_center_name="رئيسي",
    #         parent_cost_center=None,
    #         company=company.name,
    #         is_group=1
    #     )
    # )
    # doc.flags.ignore_mandatory = True
    # doc.insert(ignore_permissions=True)

    main_cost_center = frappe.get_value(
        "Cost Center",
        dict(
            company=company.name,
            cost_center_name=("like", "%رئيسي%")
        ),
        "name"
    )

    current_file = get_file_path(payment_details)

    journal_entry = frappe.get_doc(
        dict(
            doctype="Journal Entry",
            title="القيد الإفتتاحي لسنة ٢٠٢١",
            voucher_type="Journal Entry",
            naming_series="JV-",
            posting_date="2021-01-01",
            company=company.name,
            user_remark="القيد الإفتتاحي لسنة ٢٠٢١",
            multi_currency=0,
            remark="القيد الإفتتاحي لسنة ٢٠٢١",
            bill_date="2020-12-31",
            third_party_creation="2021-01-01",
            accounts=[],
            is_opening="Yes",
        )
    )
    import re
    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        for row in spamreader:
            if row[0] == "Account" or not row[0]:
                continue
            debit = float(re.sub(r'\s', '', row[1].replace(" ", "").replace("-", "").replace(",", "").replace("\\t",
                                                                                                              "").rstrip()) or 0)
            credit = float(re.sub(r'\s', '', row[2].replace(" ", "").replace("-", "").replace(",", "").replace("\\t",
                                                                                                               "").rstrip()) or 0)
            print(debit)
            print(credit)
            # if credit == "Closing(Cr)":
            #     continue
            # if not credit.isdigit():
            #     credit = 0
            # if not debit.isdigit():
            #     debit = 0
            account = row[0]
            account = frappe.get_value(
                "Account",
                dict(
                    company=company.name,
                    name=account
                ), "name"
            )
            if debit and credit:
                journal_entry.append("accounts", dict(
                    account=account,
                    party_type=None,
                    party=None,
                    title="",
                    exchange_rate=1,
                    debit_in_account_currency=abs(0),
                    debit=abs(0),
                    journal_note="القيد الإفتتاحي",
                    credit_in_account_currency=abs(credit),
                    credit=abs(credit),
                    is_advance="No",
                    cost_center=main_cost_center
                ))
                journal_entry.append("accounts", dict(
                    account=account,
                    party_type=None,
                    party=None,
                    title="",
                    exchange_rate=1,
                    debit_in_account_currency=abs(debit),
                    debit=abs(debit),
                    journal_note="القيد الإفتتاحي",
                    credit_in_account_currency=abs(0),
                    credit=abs(0),
                    is_advance="No",
                    cost_center=main_cost_center
                ))
            else:
                journal_entry.append("accounts", dict(
                    account=account,
                    party_type=None,
                    party=None,
                    title="",
                    exchange_rate=1,
                    debit_in_account_currency=abs(debit),
                    debit=abs(debit),
                    journal_note="القيد الإفتتاحي",
                    credit_in_account_currency=abs(credit),
                    credit=abs(credit),
                    is_advance="No",
                    cost_center=main_cost_center
                ))
    journal_entry.flags.ignore_permissions = True
    journal_entry.save()

    journal_entry.submit()
