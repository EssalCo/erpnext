
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
import urllib


@frappe.whitelist(allow_guest=True)
def create_task():
    try:
        data = frappe.form_dict
        subject = data.get('subject')
        description = data.get('description')
        expected_start_date = data.get('expected_start_date')
        project = data.get('project')

        task = frappe.get_doc({
            "doctype": "Task",
            "subject": subject,
            "description": description if description!=subject else None,
            "expected_start_date": expected_start_date,
            "status": "Open",
            "project": project,
        })
        task.flags.ignore_mandatory = True
        task.insert(ignore_permissions=True)

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", )