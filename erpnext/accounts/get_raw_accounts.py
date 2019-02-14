
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


@frappe.whitelist(allow_guest=True)
def get_raw_accounts():
    try:
        accounts = frappe.get_all(
          "Account",
          fields=["*"],
         ignore_permissions=True,
         ignore_ifnull=True)
        
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", accounts=accounts)
