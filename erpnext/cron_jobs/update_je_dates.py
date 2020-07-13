# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path
from datetime import datetime


import frappe
from erpnext.utilities.hijri_date import convert_to_hijri


def execute():
    _file = "/private/files/nawat_gl_dates.csv"
    current_file = get_file_path(_file)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            if "Name" in row[0]: continue
            try:
                gl_id = row[0]
            except:
                continue
            date = str(row[1])
            if "/" in date:
                date = str(datetime.strptime(
                    str(date), '%d/%m/%Y'
                ))
            je_id = row[2]
            print gl_id
            print date
            gl_entry = frappe.get_value("GL Entry", gl_id, ["posting_date"], as_dict=True)
            if str(gl_entry.posting_date) != date:
                print date

                posting_hijri_date = convert_to_hijri(date)
                frappe.db.sql("""UPDATE `tabJournal Entry` 
                SET posting_date  = '{posting_date}', posting_hijri_date  =  '{posting_hijri_date}' WHERE name = %(name)s;""".format(
                    posting_date=date,
                    posting_hijri_date=posting_hijri_date
                ), dict(
                    name=je_id
                )
                )
                frappe.db.sql("""UPDATE `tabGL Entry`
                SET posting_date  = '{posting_date}', posting_hijri_date  =  '{posting_hijri_date}' WHERE name = %(name)s;""".format(
                    posting_date=date,
                    posting_hijri_date=posting_hijri_date
                ), dict(
                    name=gl_id
                ))

        #     journal_entry = frappe.get_value("Journal Entry", je_id, ["posting_date"], as_dict=True)
        #     posting_hijri_date = convert_to_hijri(journal_entry.posting_date)
        #     print journal_entry.posting_date
        #
        #     posting_date = str(journal_entry.posting_date)[:5] + str(journal_entry.posting_date)[8:10]  +  str(journal_entry.posting_date)[4:7]
        #     print posting_date
        #     frappe.db.sql("""UPDATE `tabJournal Entry`
        #     SET posting_date  = '{posting_date}', posting_hijri_date  =  '{posting_hijri_date}' WHERE name = %(name)s;""".format(
        #         posting_date=posting_date,
        #         posting_hijri_date=posting_hijri_date
        #     ), dict(
        #         name=_id
        #     )
        # )
        #     frappe.db.sql("""UPDATE `tabGL Entry`
        #     SET posting_date  = '{posting_date}', posting_hijri_date  =  '{posting_hijri_date}' WHERE voucher_no = %(name)s;""".format(
        #         posting_date=posting_date,
        #         posting_hijri_date=posting_hijri_date
        #     ), dict(
        #         name=_id
        #     ))
