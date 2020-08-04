# -*- coding: utf-8 -*-

import frappe


def execute():
    data = frappe.db.sql(
        """select left(j.title,7), ja.project, count(*)  from `tabJournal Entry Account` ja 
inner join `tabJournal Entry` j on j.name = ja.parent group by ja.project, left(j.title, 7) 
 having ja.project is not null and left(j.title,7) = "أساس - "
order by left(j.title,1);""", as_dict=True
    )

    print data
