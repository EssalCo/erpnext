
# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import frappe


@frappe.whitelist(allow_guest=True)
def get_parties():
    try:
        data = frappe.form_dict

        party_type = data.get('party_type')
        frappe.set_user("Administrator")
        if not frappe.db.exists("Doctype", dict(name=party_type)):
            frappe.throw("This party type does not exists")
        parties = [temp.name for temp in frappe.get_all(party_type,
                                       filters=dict(
                                       ),
                                       ignore_permissions=True,
                                       ignore_ifnull=True)]
        
    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", parties=parties)

