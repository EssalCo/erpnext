# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path
from datetime import datetime
from umalqurra.hijri_date import HijriDate


def execute():

    companies = frappe.get_list(
        "Company",
        filters=dict()
    )
    print(companies)
    company = companies[0]
    # if frappe.db.count(
    #         "Cost Center",
    #         dict(
    #             company=company.name
    #         )
    # ) != 0:
    #     doc = frappe.get_doc(
    #         "Cost Center",
    #         dict(
    #             parent_cost_center=None,
    #             company=company.name,
    #         )
    #     )
    # else:
    #     doc = frappe.get_doc(
    #         dict(
    #             doctype="Cost Center",
    #             cost_center_name=company.name,
    #             parent_cost_center=None,
    #             company=company.name,
    #             is_group=1
    #         )
    #     )
    #     doc.flags.ignore_mandatory = True
    #     try:
    #         doc.insert(ignore_permissions=True)
    #     except frappe.exceptions.DuplicateEntryError as e:
    #         print(e)
    main_cost_center = 'رئيسي - م'
    file = "/private/files/mrfq_costs_centers.csv"
    current_file = get_file_path(file)

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="مؤسسة خالد حسين مرفق العقارية"
        )
    )

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:

            # print row
            first_row = row[0]
            if not first_row:
                parent_cost_center = row[1]
                doc = frappe.get_doc(
                    dict(
                        doctype="Cost Center",
                        cost_center_name=parent_cost_center,
                        parent_cost_center=main_cost_center,
                        company=company.name,
                        is_group=1
                    )
                )
                doc.flags.ignore_mandatory = True
                try:
                    doc.insert(ignore_permissions=True)
                except frappe.exceptions.DuplicateEntryError:
                    pass
            else:
                cost_center_name = row[1]
                doc = frappe.get_doc(
                    dict(
                        doctype="Cost Center",
                        cost_center_name=cost_center_name,
                        parent_cost_center=parent_cost_center,
                        company=company.name,
                        is_group=1
                    )
                )
                try:
                    doc.insert(ignore_permissions=True)

                except frappe.exceptions.DuplicateEntryError:
                    pass