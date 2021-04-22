#!/usr/bin/python
# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe

from frappe.utils import getdate, nowdate,get_time, time_diff,time_diff_in_seconds,get_datetime,cint
from frappe import _, msgprint
from frappe.model.document import Document
from erpnext.hr.utils import set_employee_name
import datetime, calendar
from calendar import monthrange
from frappe import _
from frappe.utils import cint, cstr


@frappe.whitelist(allow_guest=True)
def read_acc():
	import csv
	with open('/home/frappe/frappe-bench/apps/erpnext/erpnext/account.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile)
		index=0
		jv = frappe.get_doc("Journal Entry","ANAM0000001")
		jv.total_debit = 22217649.40
		jv.total_credit = 22217649.40
		# aa_doc.credit = row[6]
		jv.flags.ignore_validate_update_after_submit = True
		jv.flags.ignore_account_permission = True
		jv.save(ignore_permissions=True)
		# for row in spamreader:
		# 	if row[7]:
		# 		aa=frappe.get_all("Journal Entry Account" , ['party','name','account','credit'],filters={"idx":row[7],"parent":"ANAM0000001"})
				

				# if aa:
				# 	aa_doc = frappe.get_doc("Journal Entry Account",aa[0].name)

				# 	gl =frappe.get_all("GL Entry", ['name','credit'],filters={"voucher_type":"Journal Entry","voucher_no":"ANAM0000001","account":aa[0].account,"party":aa[0].party})
				# 	gl_doc = frappe.get_doc("GL Entry",gl[0].name)
				# 	if row[6]:
						


						# print row[6]
						# # frappe.db.sql(""" update  `tabJournal Entry Account` set credit ='{0}' where name = '{1}'""".format(1,dd.name))
						# # 	frappe.db.commit()
						# aa_doc.credit_in_account_currency = row[6]
						# aa_doc.credit = row[6]
						# aa_doc.flags.ignore_validate_update_after_submit = True
						# aa_doc.flags.ignore_account_permission = True
						# aa_doc.save(ignore_permissions=True)

						# gl_doc.credit = row[6]
						# gl_doc.credit_in_account_currency = row[6]
						# gl_doc.flags.ignore_validate_update_after_submit = True
						# gl_doc.flags.ignore_account_permission = True
						# gl_doc.save(ignore_permissions=True)

					# index+=1
					# print "****"
					# print "****"
					# print "****"
					# print index


@frappe.whitelist(allow_guest=True)
def read_items():
	import csv
	with open('/home/frappe/frappe-bench/apps/erpnext/erpnext/elect.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile)
		index=0

		# gr =frappe.get_doc({"doctype" : "Item Group","item_group_name": "مواد كهربا T.D.C.O2".encode('utf-8').decode('utf-8'),"parent_item_group":"All Item Groups"})
		# gr.flags.ignore_mandatory = True
		# gr.save(ignore_permissions = True)
		for row in spamreader:
			if row[0]:
				uom=frappe.get_all("UOM" , ['name'],filters={"name":row[3]})
				if not uom:
					uom =frappe.get_doc({"doctype" : "UOM","uom_name":row[3]})
					uom.flags.ignore_mandatory = True
					uom.save(ignore_permissions = True)
				aa=frappe.get_doc({
					"doctype":"Item",
					"item_code": row[1],
					"item_name" : row[4].decode('utf-8'),
					"stock_uom" : row[3],
					"item_group" : "مواد سباكة T.D.C.O2",
					"is_stock_item":1,
					"opening_stock":0

							})
				aa.flags.ignore_mandatory = True
				aa.save(ignore_permissions = True)
				print aa.name





@frappe.whitelist(allow_guest=True)
def read_accounts():
	import csv
	with open('/home/frappe/frappe-bench/apps/erpnext/erpnext/income.csv', 'r') as csvfile:
		spamreader = csv.reader(csvfile)
		index=0
		
		for row in spamreader:
			if row[0]:
				parent_account=None
				is_group = 0
				root_type=""
				par=None
				index+=1
				


				parent=frappe.get_all("Account" , ['name'],filters={"account_number":"41"})
				if parent:
					parent_account = parent[0].name
				# if (len(row[0])<5):
				# 	print len(row[0])
				# 	is_group = 1
				# 	print row[0]
				# 	print index
				# 	if(int(row[0][0])==1) :
				# 		root_type="Asset"
				# 	if(int(row[0][0])==2):
				# 		root_type="Equity"
				# 	if(int(row[0][0])==3):
				# 		root_type="Expense"
				# 	if(int(row[0][0])==4):
				# 		root_type="Income"
				# 	print root_type


				# account_type= _(row[2].strip())
				# if row[2]== "EXPENSES":
				# 	account_type = _("Expense Account")
				# if account_type not in ["Accumulated Depreciation", "Assets", "Bank", "Cash", "Chargeable", "Cost of Goods Sold", "Depreciation", "Equity", "Expense Account", "Expenses Included In Valuation", "Fixed Assets", "Current Assets", "Income Account", "Payable", "Receivable", "Prepayments", "Round Off", "Stock", "Stock Adjustment", "Stock Received But Not Billed", "Tax", "Temporary", "Bank and Cash", "cost of revenue", "Non-current Assets", "Current Year Earnings", "Current Liabilities", "Other income"]:
				# 	account_type = "Fixed Assets"	

				# parts = [row[1].decode('utf-8').strip(), "E"]
				# parts.insert(0, cstr( row[0]).strip())
				# name =  ' - '.join(parts)



				# frappe.db.sql(""" insert into  `tabAccount` ( account_name , account_number ,account_type , is_group,root_type,account_serial,parent_account,company,name) VALUES ('{0}','{1}','{2}','{3}','{4}',0,'{5}','etehadalbshair','{6}') """.format(row[1].decode('utf-8'),row[0],account_type,is_group,root_type,parent_account , name))
				if (len(row[0])<=8):
					is_group = 1
				else:
					is_group = 0
				dd = frappe.get_doc({"doctype":"Account",
						"account_name":row[1].decode('utf-8'),
						"account_number" : row[0],
						 "is_group ":  0,
						 "root_type" : "Income",
						 "account_serial" : 0,
						 "parent_account" : parent_account,
						 "company" :"شركة الوكيل العربي المحدودة"
						 })
				dd.flags.ignore_mandatory = True
				dd.ignore_validate = True
				dd.save(ignore_permissions = True)
				# if (len(row[0])<=8):
				# 	frappe.db.sql(""" update  `tabAccount` set is_group ='{0}' where name = '{1}'""".format(1,dd.name))
				# 	frappe.db.commit()


		

							
	

