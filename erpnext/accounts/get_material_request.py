# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import erpnext
from frappe import _
import frappe


@frappe.whitelist(allow_guest=True)
def get_material_request():
    # 'account',
    try:
        data = frappe.form_dict

        company = data.get('company')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        frappe.set_user("Administrator")
        conditions = ""

        if company:
            conditions = """ WHERE `company` = '{company}' """.format(
                company=company
            )
        if from_date and to_date:
            if conditions:
                conditions += " AND "
            else:
                conditions += " WHERE"
            conditions += """ `creation` BETWEEN '{from_date}' AND '{to_date}' """.format(
                from_date=from_date,
                to_date=to_date
            )

        requests = dict((temp.id, temp) for temp in frappe.db.sql("""SELECT `NAME` AS id,
	`creation`,
	`owner`,
	`naming_series`,
	`title`,
	`material_request_type`,
	`schedule_date`,
    `company`,
    `requested_by`,
    `transaction_date`,
    `status`,
    `per_ordered`,
    `terms`,
    `workflow_state`
FROM
	`tabMaterial Request`
	{conditions};""".format(
            conditions=conditions
        ), as_dict=True))

        requests_ids = requests.keys()
        if len(requests_ids) != 0:
            items = frappe.db.sql("""SELECT `NAME` AS id,
        `parent`,
        `item_code`,
        `item_name`,
        `description`,
        `qty` AS quantity,
        `stock_uom`,
        `warehouse`,
        `schedule_date`,
        `uom`,
        `conversion_factor`,
        `stock_qty` AS stock_quantity,
        `item_group`,
        `brand`,
        `lead_time_date`,
        `sales_order`,
        `sales_order_item`,
        `project`,
        `min_order_qty` AS min_order_quantity,
        `projected_qty` AS projected_quantity,
        `actual_qty` AS actual_quantity,
        `ordered_qty` AS completed_quantity
    FROM
        `tabMaterial Request Item`
        WHERE `parent` IN %(requests_ids)s;""",dict(
                requests_ids=requests_ids
            ), as_dict=True)

        else:
            items = list()

        for item in items:
            if "items" not in requests[item.parent]:
                requests[item.parent]["items"] = list()
            requests[item.parent]["items"].append(item)
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", requests=requests.values())
