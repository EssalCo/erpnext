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

    for company in companies:
        doc = frappe.get_doc(
            dict(
                doctype="Cost Center",
                cost_center_name=company.name,
                parent_cost_center=None,
                company=company.name,
                is_group=1
            )
        )
        doc.flags.ignore_mandatory = True
        try:
            doc.insert(ignore_permissions=True)
        except frappe.exceptions.DuplicateEntryError as e:
            print(e)
        frappe.db.commit()

    return

    file = "/private/files/villas_no.csv"
    cost_centers = ["@ قسم السباكة - TDCO", "@ قسم الكهرباء - TDCO", "@قسم الانشائي - TDCO"]
    cost_centers_names = ["قسم السباكة", "قسم الكهرباء", "قسم الانشائي"]
    current_file = get_file_path(file)

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="شركة ابعاد فنية للمقاولات"
        )
    )

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            # print row
            try:
                int(row[0])
            except:
                continue
            villa = str(row[0])
            print(villa)
            doc = frappe.get_doc(
                        dict(
                            doctype="Cost Center",
                            cost_center_name="{0} - فيلا - {1}".format(
                                cost_centers_names[0],
                                villa
                            ),
                            parent_cost_center=cost_centers[0],
                            company=company.name,
                            is_group=0
                        )
            )
            doc.flags.ignore_mandatory = True
            try:
                doc.insert(ignore_permissions=True)
            except frappe.exceptions.DuplicateEntryError:
                pass

            doc = frappe.get_doc(
                dict(
                    doctype="Cost Center",
                    cost_center_name="{0} - فيلا - {1}".format(
                        cost_centers_names[1],
                        villa
                    ),
                    parent_cost_center=cost_centers[1],
                    company=company.name,
                    is_group=0
                )
            )
            doc.flags.ignore_mandatory = True
            try:
                doc.insert(ignore_permissions=True)
            except frappe.exceptions.DuplicateEntryError:
                pass

            doc = frappe.get_doc(
                dict(
                    doctype="Cost Center",
                    cost_center_name="{0} - فيلا - {1}".format(
                        cost_centers_names[2],
                        villa
                    ),
                    parent_cost_center=cost_centers[2],
                    company=company.name,
                    is_group=0
                )
            )
            doc.flags.ignore_mandatory = True
            try:
                doc.insert(ignore_permissions=True)
            except frappe.exceptions.DuplicateEntryError:
                pass
