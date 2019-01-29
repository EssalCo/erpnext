from __future__ import unicode_literals
import frappe


@frappe.whitelist(allow_guest=1)
def get_allowed_companies(user):

    if user == "Administrator":
        allowed_companies = frappe.get_list("Company",
                                            fields=["name"],
                                            ignore_permissions=True
                                            )
    else:
        allowed_companies = frappe.get_list("User Permission",
                                            filters={
                                                "allow": "Company",
                                                "user": user
                                            },
                                            fields=["for_value as name"],
                                            ignore_permissions=True
                                            )
    allowed_companies = [company["name"] for company in allowed_companies]
    return allowed_companies


@frappe.whitelist(allow_guest=1)
def set_session_company(user_id=None, company_id=None):
    if not company_id and user_id:
        company_id = get_allowed_companies(user_id)[0]
    frappe.local.session_company = company_id
    return company_id


@frappe.whitelist(allow_guest=1)
def check_if_user_using_session_company(user_id=None):
    return frappe.get_value("User Session Company", {"user": user_id}, "is_enabled") or user_id == "Administrator"

