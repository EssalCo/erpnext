# -*- coding: utf-8 -*-

import frappe

def execute():
    entries = ['00012',
               '00013',
               '00019',
               '00021',
               '00023',
               '00024',
               '00026',
               '00027',
               '00029',
               '00031',
               '00032',
               '00035',
               '00036',
               '00038',
               '00045',
               '00048',
               '00049',
               '00051',
               '00058',
               '00061',
               '00066',
               '00067',
               '00075',
               '00077',
               '00082',
               '00087',
               '00091',
               '00100',
               '00103',
               '0047-1',
               '0035-1',
               '0083-1',
               '00111',
               '00117',
               '00120',
               '00122',
               '00123',
               '00126',
               '00129',
               '00133',
               '00134',
               '00135',
               '00136',
               '00142',
               '00143',
               '00144',
               '00145',
               '00151',
               '00155',
               '00156',
               '00160',
               '00161',
               '00162',
               '00164',
               '00170',
               '00175',
               '00177',
               '00182',
               '00184',
               '00189',
               '00190',
               '00192',
               '00194',
               '00201',
               '00205',
               '00206',
               '00209',
               '00220',
               '00223',
               '00225',
               '00226',
               '00244',
               '00250',
               '00274',
               '00279'
               ]

    for entry in entries:
        jouranl_entry_id = frappe.get_list(
            "Journal Entry",
            fields=["name"],
            filters=dict(
                name=("like", "%{0}".format(entry)),

                company="أعمال النماء"
            )
        )
        print jouranl_entry_id

        frappe.db.set_value(
            "Journal Entry",
            jouranl_entry_id[0].name,
            {"do_not_merge_similar_entries": 1,
            "docstatus": 0}, None
        )
        frappe.db.sql("""delete from `tabGL Entry` where voucher_type=%s and voucher_no=%s""",
                      ("Journal Entry", jouranl_entry_id[0].name))
        journal_entry = frappe.get_doc(
            "Journal Entry",
            jouranl_entry_id[0].name
        )
        journal_entry.submit()

