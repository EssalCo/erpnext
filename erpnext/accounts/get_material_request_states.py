# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime
import erpnext
from frappe import _
import frappe


@frappe.whitelist(allow_guest=True)
def get_material_request_states():
    try:
        states = [temp.state for temp in frappe.db.sql(
            """SELECT 
fs.state
FROM tabWorkflow f 
INNER JOIN `Workflow Document State` fs ON fs.`parent` = f.`name`
WHERE f.document_type = "Material Request" AND is_active = 1;""", as_dict=True
        )]

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", states=states)
