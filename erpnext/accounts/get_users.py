# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


@frappe.whitelist(allow_guest=True)
def get_users():
    try:
        users = frappe.db.sql("""SELECT
	u.`NAME` 
FROM
	`tabUser` u 
WHERE
	u.`enabled` = 1 
	AND u.`user_type` = 'System User';""", as_dict=True)
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", users=users)
