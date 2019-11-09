# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path


def execute():
    items_groups = frappe.get_list(
        "Item Group",
        filters=dict(

        ),
        ignore_ifnull=True,
        ignore_permissions=True
    )

    for item_group in items_groups:
        count = frappe.db.count(
            "Item",
            dict(
                item_group=item_group.name
            )
        )
        if count == 0:
            try:
                doc = frappe.get_doc(
                    dict(
                        doctype="Item",
                        naming_series="ITEM-",
                        item_code=item_group.name.split(" - ")[0],
                        item_name=item_group.name.split(" - ")[1],
                        item_group=item_group.name
                    )
                )
                doc.flags.ignore_mandatory = True
                doc.insert(ignore_permissions=True)
                print item_group.name.split(" - ")[0]
            except:
                pass
    ###############
    return
    items_groups = frappe.get_list(
        "Item Group",
        filters=dict(

        ),
        ignore_ifnull=True,
        ignore_permissions=True
    )

    for item_group in items_groups:
        count = frappe.db.count(
            "Item Group",
            dict(
                parent_item_group=item_group.name
            )
        )
        if count == 0:
            frappe.db.set_value(
                "Item Group",
                item_group.name,
                "is_group",
                0
            )
    return
    items = "/private/files/items.csv"

    print("Starting Items..")

    current_file = get_file_path(items)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            try:
                serial_no = int(row[1])
            except:
                continue
            if not serial_no:
                continue
            # print row
            item_name = row[2].decode('utf-8')
            item_type = row[3].decode('utf-8')
            # children_units = int(row[4])
            parent_item = int(row[6]) if row[6] else None
            parent_name = row[7].decode('utf-8')

            if serial_no == 1015218 and parent_item == 1015218:
                parent_item = "10152"
            if serial_no == 10192 and parent_item == 10192:
                parent_item = "1019"
            if serial_no == 1022306 and not parent_item:
                parent_item = "10223"
            print serial_no
            print parent_item
            if parent_item:
                parent_item = frappe.get_value(
                    "Item Group",
                    dict(
                        item_group_name=("like", "{0} - %".format(parent_item)),
                    ),
                    "name"
                )

                if not parent_item:
                    doc = frappe.get_doc(
                        dict(
                            doctype="Item Group",
                            item_group_name="{0} - {1}".format(int(row[6]), parent_name),
                            parent_item_group="مجموعات جميع الاصناف",
                            is_group=1
                        )
                    )
                    doc.flags.ignore_mandatory = True
                    doc.insert(ignore_permissions=True)
                    parent_item = doc.name
            else:
                parent_item = "مجموعات جميع الاصناف"

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
                print serial_no
            else:
                doc = frappe.get_doc(
                    dict(
                        doctype="Item",
                        naming_series="ITEM-",
                        item_code=str(serial_no),
                        item_name=item_name,
                        item_group=parent_item
                    )
                )
                doc.flags.ignore_mandatory = True
                doc.insert(ignore_permissions=True)

                print serial_no