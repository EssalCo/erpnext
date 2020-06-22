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
    payment_details = "/private/files/opening_murbiha.csv"

    print("Starting journals..")

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="DR ABDULAZIZ HAMAD ALMASHAL"
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
            title="القيد الختامي لسنة ٢٠١٩",
            voucher_type="Journal Entry",
            naming_series="JV-",
            posting_date=datetime.now(),
            company=company.name,
            user_remark="القيد الختامي لسنة ٢٠١٩",
            multi_currency=0,
            remark="القيد الختامي لسنة ٢٠١٩",
            bill_date=datetime.now(),
            third_party_creation="القيد الختامي لسنة ٢٠١٩",
            accounts=[],
            is_opening="No",
        )
    )
    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str('"'))
        for row in spamreader:
            print row
            credit = row[2]
            debit = row[1]

            if not credit.isdigit():
                credit = 0
            if not debit.isdigit():
                debit  = float(debit)
            journal_entry.append("accounts", dict(
                account=row[1],
                party_type=None,
                party=None,
                title="",
                exchange_rate=1,
                debit_in_account_currency=abs(credit),
                debit=abs(credit),
                journal_note="القيد  الختامي",
                credit_in_account_currency=abs(credit),
                credit=abs(credit),
                is_advance="No",
                cost_center=main_cost_center
            ))

    journal_entry.save(ignore_permissions=True)