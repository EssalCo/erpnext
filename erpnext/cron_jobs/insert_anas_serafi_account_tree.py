# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path


def execute():
    accounts_tree = "/private/files/anas_account_tree.csv"

    frappe.db.sql(
        """DELETE FROM tabAccount WHERE company = 'مؤسسة أنس صيرفي';"""
    )
    company = frappe.get_doc(
        "Company",
        dict(
            company_name="مؤسسة أنس صيرفي"
        )
    )

    print("Starting Accounts..")

    current_file = get_file_path(accounts_tree)
    parent_account = None
    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            try:
                serial_no = int(row[5])
            except:
                continue
            # print row
            account_name = row[4].decode('utf-8')
            account_type = row[6].decode('utf-8')

            if account_type == "فرعي":
                is_group = 0
            else:
                is_group = 1

            parent_account_serial = str(serial_no)[:-2]
            parent_acc = None
            print parent_account_serial, '-', serial_no
            print str(is_group)
            if parent_account_serial:
                parent_acc = frappe.get_value(
                    "Account",
                    dict(
                        account_serial=parent_account_serial,
                        company=company.name
                    ),
                    "name"
                )
                if not parent_acc:
                    parent_acc = frappe.get_value(
                        "Account",
                        dict(
                            account_serial=str(serial_no)[:-1],
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
                    is_group=is_group,
                    # account_currency="SAR",
                    parent_account=parent_acc,
                    report_type="Balance Sheet",
                    root_type="Expense"
                )
            )
            doc.flags.ignore_mandatory = True
            try:
                doc.insert(ignore_permissions=True)
            except frappe.exceptions.DuplicateEntryError:
                if frappe.db.exists(
                        "Account",
                        dict(
                            company=company.name,
                            account_serial=serial_no
                        )
                ):
                    continue
                else:
                    account_name = "{0} - {1}".format(parent_account, account_name)
                    doc.name = None
                    doc.account_name = account_name
                    doc.insert(ignore_permissions=True)
