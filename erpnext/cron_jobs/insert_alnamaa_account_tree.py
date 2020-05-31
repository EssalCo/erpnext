# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path


def execute():
    accounts_tree = "/private/files/nawat_daleel.csv"

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="نواة للاستثمار العقاري"
        )
    )
    serial_no = "1"
    account_name = "الأصول"
    doc = frappe.get_doc(
        dict(
            doctype="Account",
            account_name="{0} - {1}".format(serial_no, account_name),
            account_number=None,
            account_serial=serial_no,
            company=company.name,
            is_group=1,
            # account_currency="SAR",
            parent_account=None,
            report_type="Balance Sheet",
            root_type="Expense"
        )
    )
    doc.flags.ignore_mandatory = True
    doc.insert(ignore_permissions=True)

    print("Starting Accounts..")

    current_file = get_file_path(accounts_tree)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            try:
                serial_no = int(row[0])
            except:
                continue
            # print row
            print str(serial_no)
            account_name = row[1].decode('utf-8')
            # account_type = row[2].decode('utf-8')
            parent_account_serial = row[0][:-1]
            parent_acc = frappe.get_value(
                "Account",
                dict(
                    account_serial=parent_account_serial,
                    company=company.name
                ),
                "name"
            )

            if not parent_acc:
                parent_account_serial = parent_account_serial[:-1]
                print parent_account_serial

                parent_acc = frappe.get_value(
                    "Account",
                    dict(
                        account_serial=parent_account_serial,
                        company=company.name
                    ),
                    "name"
                )
            if not parent_acc:
                parent_account_serial = parent_account_serial[:-1]
                print parent_account_serial
                parent_acc = frappe.get_value(
                    "Account",
                    dict(
                        account_serial=parent_account_serial,
                        company=company.name
                    ),
                    "name"
                )

            doc = frappe.get_doc(
                dict(
                    doctype="Account",
                    account_name="{0} - {1}".format(serial_no, account_name),
                    account_number=None,
                    account_serial=serial_no,
                    company=company.name,
                    is_group=1,
                    # account_currency="SAR",
                    parent_account=parent_acc,
                    report_type="Balance Sheet",
                    root_type="Expense"
                )
            )
            doc.flags.ignore_mandatory = True
            doc.insert(ignore_permissions=True)

    accounts = frappe.get_list(
        "Account",
        fields=["name"],
        filters=dict(
            company=company.name
        )
    )
    for account in accounts:
        if frappe.db.count(
            "Account",
            dict(
                parent=account.name
            )
        ) == 0:
            frappe.db.set_value(
                "Account",
                account.name,
                "is_group",
                0
            )



# def execute():
#     accounts_tree = "/private/files/accounts_tree_new.csv"
#
#     company = frappe.get_doc(
#         "Company",
#         dict(
#             company_name="ALNAMAA"
#         )
#     )
#
#     print("Starting Accounts..")
#
#     current_file = get_file_path(accounts_tree)
#
#     with open(current_file, 'rb') as csvfile:
#         spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
#         for row in spamreader:
#             try:
#                 serial_no = int(row[0])
#             except:
#                 continue
#             # print row
#             account_name = row[1].decode('utf-8')
#             # account_type = row[2].decode('utf-8')
#             children_units = int(row[4])
#             parent_account = int(row[5]) if row[5] else None
#
#             if parent_account:
#                 parent_acc = frappe.get_value(
#                     "Account",
#                     dict(
#                         account_name=("like", "{0} - %".format(parent_account)),
#                         company=company.name
#                     ),
#                     "name"
#                 )
#             else:
#                 parent_acc = None
#             doc = frappe.get_doc(
#                 dict(
#                     doctype="Account",
#                     account_name="{0} - {1}".format(serial_no, account_name),
#                     account_number=None,
#                     account_serial=serial_no,
#                     company=company.name,
#                     is_group=children_units > 0,
#                     # account_currency="SAR",
#                     parent_account=parent_acc,
#                     report_type="Balance Sheet",
#                     root_type="Expense"
#                 )
#             )
#             doc.flags.ignore_mandatory = True
#             try:
#                 doc.insert(ignore_permissions=True)
#             except frappe.exceptions.DuplicateEntryError:
#                 if frappe.db.exists(
#                         "Account",
#                         dict(
#                             company=company.name,
#                             account_serial=serial_no
#                         )
#                 ):
#                     continue
#                 else:
#                     account_name = "{0} - {1}".format(parent_account, account_name)
#                     doc.name = None
#                     doc.account_name = account_name
#                     doc.insert(ignore_permissions=True)
