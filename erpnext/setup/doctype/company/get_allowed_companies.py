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
