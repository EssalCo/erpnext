
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
import urllib


@frappe.whitelist(allow_guest=True)
def update_task_status():
    try:
        data = frappe.form_dict
        task_id = data.get('task_id')
        status = data.get('status')
        if status not in ("Open",
                "Working",
                "Pending Review",
                "Overdue",
                "Closed",
                "Cancelled"):
            return dict(status=False, message="Status not allowed")
        try:
            task = frappe.get_doc("Task", task_id)
        except Exception as e:
            return dict(status=False, message="Task does not exist")

        task.status = status
        task.save(ignore_permissions=True)
        frappe.db.commit()
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success")