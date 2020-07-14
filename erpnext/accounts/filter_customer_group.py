from __future__ import unicode_literals

import frappe
from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist()
def filter_customer_group(doctype, txt_ignored, searchfield_ignored, limit_start, limit_page_length, filters):
    send_msg_telegram(
        str(filters))

    if not filters.get("party_type"):
        return ()
    _filters = dict()
    if filters.get('party'):
        _filters["{0}_name".format(filters["party_type"].lower())] = ("like", "%{0}%".format(filters['party']))
    if filters.get('party_type') == "Customer":
        if filters.get('customer_group'):
            if frappe.get_value(
                    "Customer Group",
                    filters['customer_group'],
                    "parent_customer_group"
            ):
                _filters = dict(
                    customer_group=filters['customer_group']
                )
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


def get_customer_list(doctype, txt, searchfield, start, page_len, filters):
    filter_list = []

    if isinstance(filters, dict):
        for key, val in filters.items():
            if isinstance(val, (list, tuple)):
                filter_list.append([doctype, key, val[0], val[1]])
            else:
                filter_list.append([doctype, key, "=", val])
    # elif isinstance(filters, list):
    #     filter_list.extend(filters)
    is_customer = False

    for d in filters:
        if d[3] and d[0] == "Customer" and d[1] == "customer_group":
            if frappe.get_value(
                    "Customer Group",
                    d[3],
                    "parent_customer_group"
            ):
                filter_list.append(["Customer", "customer_group", "=", d[3]])
            is_customer = True
    if doctype == "Customer": is_customer = True
    if searchfield and txt:
        filter_list.append([doctype, searchfield, "like", "%%%s%%" % txt])
    if is_customer:
        fields = ["name", "{0}_name".format(doctype.lower()), "customer_group"]
        customers = frappe.db.get_list(doctype, filters= filter_list,
                                                   fields = fields,
                                                   limit_start=start, limit_page_length=page_len)
        result = []
        for customer in customers:
            result.append(
                (customer.name, "{0} - {1}".format(
                    customer["{0}_name".format(doctype.lower().lower())], customer.customer_group))
            )
        return ((temp) for temp in result)
    elif doctype == "Employee":
        fields = ["name", "{0}_name".format(doctype.lower())]
        filter_list.append([doctype, "employee_name", "like", "%%%s%%" % txt])
        customers = frappe.db.get_list(doctype, or_filters= filter_list,
                                       fields = fields,
                                       limit_start=start, limit_page_length=page_len)
        result = []
        for customer in customers:
            result.append(
                (customer.name, "{0}".format(
                    customer["{0}_name".format(doctype.lower().lower())]))
            )
        return ((temp) for temp in result)
    else:
        fields = ["name", "{0}_name".format(doctype.lower())]

    return frappe.db.get_list(doctype, filters= filter_list,
                                          fields = fields,
                                          limit_start=start, limit_page_length=page_len, as_list=True)