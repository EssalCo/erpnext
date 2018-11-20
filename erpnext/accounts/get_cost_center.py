# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import frappe


@frappe.whitelist(allow_guest=True)
def get_cost_center():
    # 'account',
    try:
        data = frappe.form_dict

        account = data.get('account')
        frappe.set_user("Administrator")
        
        company = frappe.get_value("Account", account, "company")
        
        cost_centers = frappe.get_list("Cost Center",
                                       fields=["name", "cost_center_name"],
                                       filters=dict(
                                           company=company,
                                           is_group=0
                                       ),
                                       ignore_permissions=True,
                                       ignore_ifnull=True)
        
        cost_centers_list = [temp.cost_center_name for temp in cost_centers]
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", cost_centers=cost_centers_list, cost_centers_dict=cost_centers)

