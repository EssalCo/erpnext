# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import math
from datetime import datetime, timedelta

import frappe


def execute():
    accounts = frappe.db.sql(
        """SELECT `name` FROM 
        `tabAccount` WHERE `company` = %(company)s ORDER BY `creation` DESC;""", as_dict=True
    )

    for acc in accounts:
        account = frappe.get_doc("Account", acc.name)
        account.get_account_serial()
        account.save(ignore_permissions=True)