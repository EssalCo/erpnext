# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import erpnext
from frappe import _
import frappe


@frappe.whitelist(allow_guest=True)
def get_activity_log():
    # 'account',
    try:
        data = frappe.form_dict

        user_id = data.get('user_id')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        frappe.set_user("Administrator")

        logs = frappe.db.sql("""SELECT `NAME` AS id,
	`creation`,
	`full_name`,
	`operation`,
	`subject` ,
	`status`,
    `user`
FROM
	`tabActivity Log`
	WHERE 
	`creation` BETWEEN %(from_date)s AND %(to_date)s
	{user_condition};""".format(
            user_condition=" AND `user` = '{0}'".format(user_id) if user_id else ""
        ), dict(from_date=from_date, to_date=to_date), as_dict=True)

        for log in logs:
            log.full_name = _(log.full_name, "ar")
            log.operation = _(log.operation, "ar")

            log.subject = _(log.subject, "ar")
            log.status = _(log.status, "ar")
            log.user = _(log.user, "ar")

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", logs=logs)
