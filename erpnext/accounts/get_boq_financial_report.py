# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals

import frappe


# from erpnext.accounts.doctype.accounting_dimension.accounting_dimension import get_accounting_dimensions
# from erpnext.accounts.report.utils import get_currency, convert_to_presentation_currency


@frappe.whitelist(allow_guest=True)
def execute():
    try:

        # project
        # from_date
        # to_date
        filters = list()

        data = frappe.form_dict
        project = data.get('project')
        if project:
            filters.append(["Bill of Quantities", "project", "=", project])

        from_date = data.get('from_date')
        if from_date:
            filters.append(["Bill of Quantities", "posting_date", ">=", from_date])

        to_date = data.get('to_date')
        if to_date:
            filters.append(["Bill of Quantities", "posting_date", "<", to_date])

        if not filters:
            data = frappe.form_dict.data
            project = data.get('project')
            if project:
                filters.append(["Bill of Quantities", "project", "=", project])

            from_date = data.get('from_date')
            if from_date:
                filters.append(["Bill of Quantities", "posting_date", ">=", from_date])

            to_date = data.get('to_date')
            if to_date:
                filters.append(["Bill of Quantities", "posting_date", "<", to_date])
        frappe.set_user("Administrator")
        data = frappe.get_list(
            "Bill of Quantities",
            fields=[
                "name",
                "bill_of_quantities_name",
                "company",
                "project",
                "posting_date",
                "type",
                "customer",
                "estimated_sell",
                "estimated_cost",
                "profit_margin",
                "currency",
                "conversion_rate",
                "buying_price_list",
                "price_list_currency",
                "plc_conversion_rate",
                "ignore_pricing_rule",
                "base_total",
                "base_net_total",
                "total",
                "net_total",
                "total_net_weight",
                "taxes_and_charges",
                "shipping_rule",
                "other_charges_calculation",
                "base_taxes_and_charges_added",
                "base_taxes_and_charges_deducted",
                "base_total_taxes_and_charges",
                "taxes_and_charges_added",
                "taxes_and_charges_deducted",
                "total_taxes_and_charges",
                "additional_discount_percentage",
                "discount_amount",
                "apply_discount_on",
                "base_grand_total",
                "base_rounding_adjustment",
                "base_in_words",
                "base_rounded_total",
                "grand_total",
                "rounding_adjustment",
                "rounded_total",
                "in_words",
                "disable_rounded_total",
                "material_request_total",
                "tool_request_total",
                "labor_total",
                "current_total_cost",
            ],
            filters=filters,
            ignore_permissions=True,
            ignore_ifnull=True
        )
    except Exception as e:
        import traceback

        return dict(status=False, message=traceback.format_exc())

    return dict(status=True, message="Success", report=data)
