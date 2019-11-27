# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from erpnext.utilities.send_telegram import send_msg_telegram
from operator import itemgetter

import frappe
import urllib


@frappe.whitelist(allow_guest=True)
def get_fiscal_years():
    # ‘company_name’

    try:

        data = frappe.form_dict
        company_name = data.get('company_name')
        send_msg_telegram(company_name)

        # company_name = urllib.unquote(company_name)
        # send_msg_telegram(company_name)
        fiscal_year_companies = [temp.parent for temp in frappe.get_list(
            "Fiscal Year Company",
            fields=["parent"],
            filters=dict(
                company=company_name
            ),
            ignore_permissions=True,
            ignore_ifnull=True
        )]
        send_msg_telegram(str(fiscal_year_companies))

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
        send_msg_telegram(str(years))

        for year in years:
            year.year = int(year.year)
            
        years = sorted(years, key=itemgetter('year'), reverse=True)

    except Exception as e:
        import traceback
        send_msg_telegram(traceback.format_exc())
        return dict(status=False, message=str(e))

    return dict(status=True, message="Success", years=years, years_list=[temp.year for temp in years])
