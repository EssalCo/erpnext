# -*- coding: utf-8 -*-

import frappe


def execute():
    data = frappe.db.sql(
        """select left(j.title,7) as title_t, ja.project, ja.name, j.name as voucher_no  from `tabJournal Entry Account` ja 
inner join `tabJournal Entry` j on j.name = ja.parent 
 having ja.project is not null and title_t = "أساس - "
order by left(j.title,1);""", as_dict=True
    )

    # print data
    print len(data)

    for temp in data:
        frappe.db.sql(
            """UPDATE `tabJournal Entry Account` SET project = NULL WHERE parent = %(voucher_no)s""", dict(
                voucher_no=temp.voucher_no
            )
        )

        frappe.db.sql(
            """UPDATE `tabGL Entry` SET project = NULL WHERE voucher_no = %(voucher_no)s""", dict(
                voucher_no=temp.voucher_no
            )
        )
