# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import frappe

from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist(allow_guest=True)
def get_companies():
    try:

        companies = [temp.name for temp in frappe.get_all("Company",
                                                          filters=dict(
                                                          ),
                                                          ignore_permissions=True,
                                                          ignore_ifnull=True)]

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", companies=companies)


@frappe.whitelist(allow_guest=True)
def get_users():
    try:

        employees = frappe.get_list("Employee",
                                    fields=["*"],
                                    filters=dict(
                                        company="مؤسسة أنس صيرفي"
                                    ),
                                    ignore_permissions=True,
                                    ignore_ifnull=True)
        users = frappe.get_list("User",
                                fields=["*"],
                                filters=dict(
                                    name=("in", [temp.user_id for temp in employees])
                                ),
                                ignore_permissions=True,
                                ignore_ifnull=True)
        types = frappe.get_list("Employment Type",
                                fields=["*"],
                                filters=dict(
                                ),
                                ignore_permissions=True,
                                ignore_ifnull=True)

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", users=users, employees=employees, types=types)


