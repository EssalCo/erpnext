
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
import urllib


@frappe.whitelist(allow_guest=True)
def get_all_tasks():
    try:
        data = frappe.form_dict
        project = urllib.unquote(str(data.get('project'))).decode('utf-8', 'replace') if data.get('project') else None
        company = urllib.unquote(str(data.get('company'))).decode('utf-8', 'replace') if data.get('company') else None
        frappe.set_user("Administrator")
        _filters = dict(
            company=company
        )
        if project:
            _filters['project'] = project
        tasks = frappe.get_list(
            "Task",
            fields=[
                "subject",
                "project",
                "is_group",
                "status",
                "priority", # Low
                # Medium
                # High
                # Urgent
                "parent_task",
                "exp_start_date",
                "expected_time",
                "task_weight",
                "exp_end_date",
                "progress",
                "is_milestone",
                "description",
                "depends_on_tasks",
                "act_start_date",
                "actual_time",
                "act_end_date",
                "total_costing_amount",
                "total_expense_claim",
                "total_billing_amount",
                "review_date",
                "closing_date",
                "company",
            ],
            filters=_filters,
            ignorer_permissions=True,
            ignore_ifnull=True
            )

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", parties=tasks)