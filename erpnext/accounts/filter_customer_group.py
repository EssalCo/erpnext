from __future__ import unicode_literals

import frappe
from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist()
def filter_customer_group(doctype, txt_ignored, searchfield_ignored, limit_start, limit_page_length, filters):
    send_msg_telegram(
        str(filters))

    if not filters.get("party_type"):
        return ()
    if filters.get('party_type') == "Customer":
        if filters.get('customer_group'):
                _filters = dict(
                customer_group=filters['customer_group']
            )
        else:
            _filters = dict()
    else:
        _filters = dict()
    # send_msg_telegram(str(filters))
    if filters['party_type'] == "Customer":
        customers = frappe.get_all(
            filters["party_type"],
            fields=[
                "name",
                "{0}_name".format(filters["party_type"].lower()),
                "customer_group"
            ],
            filters=_filters,
            ignore_ifnull=1,
            ignore_permissions=1
        )
        result = []
        for customer in customers:
            result.append(
                (customer.name, "{0} - {1}".format(
                    customer["{0}_name".format(filters["party_type"].lower())], customer.customer_group))
            )
    else:
        customers = frappe.get_all(
            filters["party_type"],
            fields=[
                "name",
                "{0}_name".format(filters["party_type"].lower())
            ],
            filters=_filters,
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
