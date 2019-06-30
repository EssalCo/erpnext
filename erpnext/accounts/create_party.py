# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import frappe


@frappe.whitelist(allow_guest=True)
def create_party():
    # 'party_type',
    # 'party_name' ,
    # 'party_phone',
    # 'party_email'
    
    try:
        party_type = frappe.form_dict['party_type']
        party = frappe.get_doc(
            dict(
                doctype=party_type
            )
        )
        party.insert(ignore_permissions=True)
        frappe.db.commit()

        return dict(status=True, message="Party is added successfully")
    except Exception as e:
        return dict(status=False, message=str(e))

