# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import frappe



def execute():
    parent_account = "102010201 - مصرف الراجحي - أع ن"
    company = "أعمال النماء"
    last_existing_serial = frappe.db.sql("""SELECT account_serial, account_serial_x, name FROM
      `tabAccount` WHERE
       account_serial = (
    SELECT 
        MAX(account_serial * 1) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s);""", (company, parent_account), as_dict=True)
    print(last_existing_serial)
    last_existing_serial = frappe.db.sql("""
    SELECT 
        MAX(account_serial * 1) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s;""", (company, parent_account), as_dict=True)

    print(last_existing_serial)
    last_existing_serial = frappe.db.sql("""
    SELECT 
        account_serial, account_serial * 1 AS maxi, account_serial_x, name
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s;""", (company, parent_account), as_dict=True)
    for i in last_existing_serial:
        print(i)

    frappe.db.set_value(
        "Account",
        "102010201 - مصرف الراجحي - أع ن",
        "account_serial",
        "102010201"
    )