# -*- coding: utf-8 -*-

import frappe


def execute():
    x = frappe.db.sql(
        """SELECT `tabGL Entry`.posting_date, `tabGL Entry`.account, `tabGL Entry`.party_type, `tabGL Entry`.party,
                `tabGL Entry`.voucher_type, `tabGL Entry`.voucher_no, COALESCE(`tabGL Entry`.cost_center, `tabGL Entry`.cost_center) AS cost_center, `tabGL Entry`.project,
                `tabGL Entry`.against_voucher_type, `tabGL Entry`.against_voucher, `tabGL Entry`.account_currency,
                `tabGL Entry`.remarks, `tabGL Entry`.against, `tabGL Entry`.is_opening , sum(`tabGL Entry`.debit) as debit, sum(`tabGL Entry`.credit) as credit,
   round(sum(`tabGL Entry`.debit_in_account_currency), 4) as debit_in_account_currency,
   round(sum(`tabGL Entry`.credit_in_account_currency), 4) as  credit_in_account_currency
            from `tabGL Entry`
            where `tabGL Entry`.company="ALNAMAA" and `tabGL Entry`.party_type="Supplier"  and party="مؤسسة سالم باطيب لمواد البناء"  group by `tabGL Entry`.voucher_type, `tabGL Entry`.voucher_no, `tabGL Entry`.account, `tabGL Entry`.cost_center 
            order by `tabGL Entry`.posting_date, `tabGL Entry`.account;""", as_dict=True
    )

    print len(x)