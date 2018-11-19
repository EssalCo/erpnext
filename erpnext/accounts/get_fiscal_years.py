# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import traceback

import frappe
# from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist(allow_guest=True)
def get_fiscal_years():
    # ‘company_name’

    try:

        data = frappe.form_dict
        company_name = data.get('company_name')
        fiscal_year_companies = [temp.parent for temp in frappe.get_list(
            "Fiscal Year Company",
            fields=["parent"],
            filters=dict(
                company=company_name
            ),
            ignore_permissions=True,
            ignore_ifnull=True
        )]
        years = frappe.get_all(
            "Fiscal Year",
            fields=[
                "year",
                "year_start_date",
                "year_end_date",

            ],
            filters=dict(
                disabled=0,
                name=("in", fiscal_year_companies)
            ),
            ignore_permissions=True,
            ignore_ifnull=True)

    except Exception as e:
        return dict(status=False, message=str(e))

    return dict(status=True, message="Success", years=years)
