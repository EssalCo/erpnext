# -*- coding: utf-8 -*-

import frappe


def execute():

    to_be_updated = frappe.db.sql(
        """select parent, fieldname,
	(select issingle from tabDocType dt
	where dt.name = df.parent) as issingle
from tabDocField df
where
	df.options="Account" and df.fieldtype='Link' HAVING issingle = 0 ;"""
    )

    for temp in to_be_updated:

        test = frappe.db.sql(
            """SELECT CONCAT(TRIM(TRAILING '- نلا' FROM {field}), "- N") as new, {field}  FROM `tab{doctype}` 
    WHERE {field} IS NOT NULL AND {field} LIKE "%- نلا";""".format(
                doctype=temp.parent,
                field=temp.fieldname
            )
        )
        print test
        continue
        frappe.db.sql(
            """UPDATE `tab{doctype}` SET {field} = CONCAT(TRIM(TRAILING '- نلا' FROM {field}), "- N")
    WHERE {field} IS NOT NULL AND {field} LIKE "%- نلا";""".format(
                doctype=temp.parent,
                field=temp.fieldname
            )
        )
        print