from __future__ import unicode_literals

import frappe


@frappe.whitelist()
def filter_customer_group(doctype, txt_ignored, searchfield_ignored, limit_start, limit_page_length, filters):

    if filters.get('customer_group') and filters.get('party_type') == "Customer":
        filters = dict(
            customer_group=filters['customer_group']
        )
    else:
        filters = dict()
    customers = frappe.get_all(
        "Customer",
        fields=[
            "name",
            "customer_name",
            "customer_group",
            "territory"
        ],
        filters=filters,
        ignore_ifnull=1,
        ignore_permissions=1
    )
    result = []
    for customer in customers:
        result.append(
            (customer.name, "{0} - {1} - {2}".format(customer.customer_name, customer.customer_group, customer.territory))
        )
    if not result:
        return ()
    return ((temp) for temp in result)
