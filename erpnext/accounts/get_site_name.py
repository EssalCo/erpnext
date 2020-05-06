import frappe


@frappe.whitelist()
def get_site_name():
    from frappe.utils import get_site_name
    site_name = get_site_name(frappe.local.request.host)
    return site_name