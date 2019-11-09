# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path


def execute():
    items = "/private/files/items.csv"

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="ALNAMAA"
        )
    )

    print("Starting Items..")

    current_file = get_file_path(items)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            try:
                serial_no = int(row[0])
            except:
                continue
            # print row
            item_name = row[1].decode('utf-8')
            item_type = row[2].decode('utf-8')
            # children_units = int(row[4])
            parent_item = int(row[5]) if row[5] else None
            if parent_item:
                parent_item = frappe.get_value(
                    "Item Group",
                    dict(
                        item_group_name=("like", "{0} - %".format(parent_item)),
                    ),
                    "name"
                )
            else:
                parent_item = None
            if item_type != "جزئى/تحليلى":

                doc = frappe.get_doc(
                    dict(
                        doctype="Item Group",
                        item_group_name="{0} - {1}".format(serial_no, item_name),
                        parent_item_group=parent_item,
                        is_group=item_type != "جزئى/تحليلى"
                    )
                )
                doc.flags.ignore_mandatory = True
                doc.insert(ignore_permissions=True)
            else:
                doc = frappe.get_doc(
                    dict(
                        doctype="Item",
                        naming_series="ITEM-",
                        item_code=serial_no,
                        item_name=item_name,
                        item_group=parent_item
                    )
                )
                doc.flags.ignore_mandatory = True
                doc.insert(ignore_permissions=True)