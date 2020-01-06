# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import frappe
from erpnext.utilities.send_telegram import send_msg_telegram


@frappe.whitelist(allow_guest=True)
def get_cost_center():
    # 'account',
    try:
        data = frappe.form_dict
        send_msg_telegram("data: " + str(data) + " " + type(data))

        account = data.get('account')
        frappe.set_user("Administrator")
        send_msg_telegram(str(data))
        company = frappe.get_value("Account", account, "company") or data.get('company') or data.get('company_name')
        if not company:
            send_msg_telegram("get_cost_center: account: {0}".format(str(account)))

            # return dict(status=False, message="You did not specify correct account")
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
        import traceback
        send_msg_telegram(traceback.format_exc())
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", cost_centers=cost_centers_list, cost_centers_dict=cost_centers)

