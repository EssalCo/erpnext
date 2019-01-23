from __future__ import unicode_literals
import frappe
from .get_allowed_companies import get_allowed_companies


@frappe.whitelist(allow_guest=1)
def set_session_company(user_id=None, company_id=None):
    if not company_id and user_id:
        company_id = get_allowed_companies(user_id)[0]
    frappe.local.session_company = company_id
    return company_id