
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


@frappe.whitelist(allow_guest=True)
def get_party_types():
    try:
        party_types = [temp.name for temp in frappe.get_all("Party Type",
                                       filters=dict(
                                       ),
                                       ignore_permissions=True,
                                       ignore_ifnull=True)]
        
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", party_types=party_types)

