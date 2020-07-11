# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path


def execute():

    _file = "/private/files/nawat_ledger_notes.csv"
    current_file = get_file_path(_file)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            try:
                gl_id = row[0]
            except:
                continue

            print gl_id
            try:
                note = row[1]
            except: continue
            frappe.db.sql(
                """UPDATE `tabGL Entry` SET journal_note = %(journal_note)s WHERE name = %(name)s AND (journal_note IS NULL OR journal_note = "");""", dict(
                    journal_note=note,
                    name=gl_id
                )
            )