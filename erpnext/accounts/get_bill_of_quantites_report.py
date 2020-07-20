# Copyright (c) 2013, AHMED ABDELRAHMAN and contributors
# For license information, please see license.txt

from __future__ import unicode_literals

import frappe
from frappe import _


@frappe.whitelist(allow_guest=True)
def execute():
    try:

        # project
        data = frappe.form_dict
        project = data.get('project')
        if not project:
            data = frappe.form_dict.data
            project = data.get('project')
        frappe.set_user("Administrator")

        filters = dict(project=project)
        columns = get_columns(filters)
        for temp in columns:
            temp = temp.split(":")[0]
        data = get_data(filters)

    except Exception as e:
        return dict(status=False, message=str(e))

    return dict(status=True, message="Success", report=dict(data=data, columns=columns))


# def execute(filters=None):
#     columns = get_columns(filters)
#     data = get_data(filters)
#     return columns, data


def get_columns(filters):
    """return columns based on filters"""

    columns = [_("Item") + ":Link/Item:100"] + [_("Item Name") + "::150"] + [_("Description") + "::150"] + \
              [_("Warehouse") + ":Link/Warehouse:100"] + [_("Quantity Accepted") + ":Float:90"] + \
              [_("Material Request") + ":Float:80"] + [_("Purchase Order") + ":Float:80"] + [
                  _("Purchase Receipt") + ":Float:80"] + [_("Project") + ":Link/Project:100"]

    return columns


def get_conditions(filters):
    conditions = ""
    # ~ if not filters.get("from_date"):
    # ~ frappe.throw(_("'From Date' is required"))

    if filters.get("bill_of_quantities"):
        conditions += " and bqi.parent <= '%s'" % filters["bill_of_quantities"]
    if filters.get("project"):
        conditions += " and bqi.project <= '%s'" % filters["project"]
    # ~ else:
    # ~ frappe.throw(_("'To Date' is required"))

    return conditions


def get_data(filters):
    conditions = get_conditions(filters)
    boq_list = frappe.db.sql("""
		select bqi.item_code,
		bqi.item_name,
		bqi.description,
		bqi.warehouse,
		bqi.qty,
		sum(mri.qty),
		sum(poi.qty),
		sum(pri.qty),
		bqi.project
		from `tabBill of Quantities Item` bqi
		left JOIN `tabMaterial Request Item` mri 
		on bqi.project = mri.project and bqi.item_name =mri.item_name
		left JOIN `tabPurchase Order Item` poi 
		on bqi.project = poi.project and bqi.item_name =poi.item_name
		left JOIN `tabPurchase Receipt Item` pri 
		on bqi.project = pri.project and bqi.item_name =pri.item_name
		where 
		bqi.docstatus < 2 
		and mri.docstatus < 2 
		and poi.docstatus < 2 
		and pri.docstatus < 2 
		%s
		group by bqi.item_code, bqi.project
		order by bqi.item_code, bqi.project""" %
                             conditions)

    return boq_list
