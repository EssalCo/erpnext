# -*- coding: utf-8 -*-


import  frappe


def execute():
    return
    company = "أعمال النماء"
    frappe.db.sql("""delete from `tabGL Entry` where voucher_type='Journal Entry' and company = '{0}';""".format(
        company
    ))

    frappe.db.sql("""delete from `tabJournal Entry` where company = '{0}';""".format(
        company
    ))

    frappe.db.sql("""delete from `tabSeries` where name = 'ANAM';""")