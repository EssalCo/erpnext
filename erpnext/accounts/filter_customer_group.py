from __future__ import unicode_literals

import frappe
# from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist()
def filter_customer_group(doctype, txt_ignored, searchfield_ignored, limit_start, limit_page_length, filters):
    # send_msg_telegram(
    #     str(filters))

    if not filters.get("party_type"):
        return ()
    if filters.get('customer_group') and filters.get('party_type') == "Customer":
        filters = dict(
            customer_group=filters['customer_group']
        )
    else:
        filters = dict()
    # send_msg_telegram(str(filters))
    customers = frappe.get_all(
        filters["party_type"],
        fields=[
            "name",
            "{0}_name".format(filters["party_type"].lower())
        ],
        filters=filters,
        ignore_ifnull=1,
        ignore_permissions=1
    )
    result = []
    for customer in customers:
        result.append(
            (customer.name, "{0}".format(customer["{0}_name".format(filters["party_type"].lower())]))
        )
    if not result:
        return ()
    return ((temp) for temp in result)
