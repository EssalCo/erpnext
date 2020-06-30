# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe
import urllib


@frappe.whitelist(allow_guest=True)
def get_projects():
    try:
        data = frappe.form_dict
        company = data.get('company')

        filters = dict()
        if company and '%' in company:
            company = urllib.unquote(str(data['company'])).decode('utf-8', 'replace')

            filters['company'] = company

        frappe.set_user("Administrator")

        projects = frappe.get_all("Project",
                                  fields=[
                                      "name",
                                      "project_name",
                                      "status",
                                      "project_type",
                                      "is_active",
                                      "percent_complete_method",
                                      "priority",
                                      "expected_start_date",
                                      "expected_end_date",
                                      "percent_complete",
                                      "customer",
                                      "sales_order",
                                      "notes",
                                      "actual_start_date",
                                      "actual_time",
                                      "actual_end_date",
                                      "estimated_costing",
                                      "total_costing_amount",
                                      "total_expense_claim",
                                      "total_purchase_cost",
                                      "company",
                                      "total_sales_amount",
                                      "total_billable_amount",
                                      "total_billed_amount",
                                      "total_consumed_material_cost",
                                      "cost_center",
                                      "gross_margin",
                                      "per_gross_margin"

                                  ],
                                  filters=filters,
                                  ignore_permissions=True,
                                  ignore_ifnull=True)

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", projects=projects, project_ids=[temp.name for temp in projects])
