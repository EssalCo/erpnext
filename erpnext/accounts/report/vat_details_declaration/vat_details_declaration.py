# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.utils import flt
from frappe import msgprint, _

def execute(filters=None):
	return _execute(filters)

def _execute(filters=None, additional_table_columns=None, additional_query_columns=None):
	if not filters: filters = {}
	data = []
	jv_list = get_je_invoices(filters, additional_query_columns)

	invoice_list = get_pi_invoices(filters, additional_query_columns)
	columns, expense_accounts, tax_accounts = get_columns(invoice_list, additional_table_columns)
	
	for inv in jv_list:
		party_name = inv.party
		tax_id = inv.tax_id
		if inv.party and inv.party_type :
			party_doc = frappe.get_doc(inv.party_type,inv.party)
			if inv.party_type == "Supplier":
				party_name = party_doc.supplier_name
			if inv.party_type == "Customer":
				party_name = party_doc.customer_name
			if not tax_id or tax_id =="":
				tax_id = party_doc.tax_id
			
		row = [inv.name, inv.posting_date, inv.party]
		tax= -1*inv.debit_in_account_currency if inv.debit_in_account_currency  != 0 else inv.credit_in_account_currency
		
			
		row += [
				inv.project,
				None, None, inv.journal_note,inv.total_debit-tax,tax,inv.total_debit
			]
			
			
		data.append(row)
		
	if invoice_list:


		invoice_expense_map = get_invoice_expense_map(invoice_list)
		invoice_expense_map, invoice_tax_map = get_pi_invoice_tax_map(invoice_list,
			invoice_expense_map, expense_accounts)
		invoice_po_pr_map = get_invoice_po_pr_map(invoice_list)
		suppliers = list(set([d.supplier for d in invoice_list]))
		supplier_details = get_supplier_details(suppliers)

		company_currency = frappe.db.get_value("Company", filters.company, "default_currency")

		
	
		for inv in invoice_list:
			# invoice details
			project = list(set(invoice_po_pr_map.get(inv.name, {}).get("project", [])))

			row = [inv.name, inv.posting_date, inv.supplier]

			if additional_query_columns:
				for col in additional_query_columns:
					row.append(inv.get(col))

			row += [
				 ", ".join(project),
				inv.bill_no, inv.bill_date, inv.remarks
			]

			# map expense values
			base_net_total = 0
			for expense_acc in expense_accounts:
				expense_amount = flt(invoice_expense_map.get(inv.name, {}).get(expense_acc))
				base_net_total += expense_amount

			# net total
			row.append(base_net_total or inv.base_net_total)

			# tax account
			total_tax = 0
			for tax_acc in tax_accounts:
				if tax_acc not in expense_accounts:
					tax_amount = flt(invoice_tax_map.get(inv.name, {}).get(tax_acc))
					total_tax += tax_amount

			# total tax, grand total, outstanding amount & rounded total
			row += [total_tax, inv.base_grand_total, flt(inv.base_grand_total, 2)]
			data.append(row)
	
	
	#sales Invoicee
	invoice_si_list = get_si_invoices(filters, additional_query_columns)
	income_accounts, tax_accounts = get_si_columns(invoice_si_list, additional_table_columns)

	if  invoice_si_list:
		invoice_income_map = get_invoice_income_map(invoice_si_list)
		invoice_income_map, invoice_tax_map = get_invoice_tax_map(invoice_si_list,
			invoice_income_map, income_accounts)
		#Cost Center & Warehouse Map
		invoice_cc_wh_map = get_invoice_cc_wh_map(invoice_si_list)
		invoice_so_dn_map = get_invoice_so_dn_map(invoice_si_list)
		company_currency = frappe.db.get_value("Company", filters.get("company"), "default_currency")
		mode_of_payments = get_mode_of_payments([inv.name for inv in invoice_si_list])

		for inv in invoice_si_list:
			# invoice details
			sales_order = list(set(invoice_so_dn_map.get(inv.name, {}).get("sales_order", [])))
			delivery_note = list(set(invoice_so_dn_map.get(inv.name, {}).get("delivery_note", [])))
			cost_center = list(set(invoice_cc_wh_map.get(inv.name, {}).get("cost_center", [])))
			warehouse = list(set(invoice_cc_wh_map.get(inv.name, {}).get("warehouse", [])))

			row = [
				inv.name, inv.posting_date, inv.customer
			]

			if additional_query_columns:
				for col in additional_query_columns:
					row.append(inv.get(col))

			row += [
				", ".join(project),inv.po_no, inv.po_date, inv.remarks
			]
			# map income values
			base_net_total = 0
			for income_acc in income_accounts:
				income_amount = flt(invoice_income_map.get(inv.name, {}).get(income_acc))
				base_net_total += income_amount

			# net total
			row.append(base_net_total or inv.base_net_total)

			# tax account
			total_tax = 0
			for tax_acc in tax_accounts:
				if tax_acc not in income_accounts:
					tax_amount = flt(invoice_tax_map.get(inv.name, {}).get(tax_acc))
					total_tax += tax_amount

			# total tax, grand total, outstanding amount & rounded total
			row += [total_tax, inv.base_grand_total, inv.base_rounded_total, inv.outstanding_amount]

			data.append(row)
		
	return columns, data


def get_columns(invoice_list, additional_table_columns):
	"""return columns based on filters"""
	columns = [
		_("Invoice") + ":Data:120", _("Posting Date") + ":Date:80",
		_("Party") + "::120"]

	if additional_table_columns:
		columns += additional_table_columns

	columns += [
		  _("Project") + ":Link/Project:80",
		_("Bill No") + "::120", _("Bill Date") + ":Date:80", _("Remarks") + "::150"
	]
	expense_accounts = tax_accounts = expense_columns = tax_columns = []

	if invoice_list:
		expense_accounts = frappe.db.sql_list("""select distinct expense_account
			from `tabPurchase Invoice Item` where docstatus = 1
			and (expense_account is not null and expense_account != '')
			and parent in (%s) order by expense_account""" %
			', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))

		tax_accounts = 	frappe.db.sql_list("""select distinct account_head
			from `tabPurchase Taxes and Charges` where parenttype = 'Purchase Invoice'
			and docstatus = 1 and (account_head is not null and account_head != '')
			and category in ('Total', 'Valuation and Total')
			and parent in (%s) order by account_head""" %
			', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))


	expense_columns = [(account + ":Currency/currency:120") for account in expense_accounts]
	for account in tax_accounts:
		if account not in expense_accounts:
			tax_columns.append(account + ":Currency/currency:120")

	columns = columns  + [_("Net Total") + ":Currency/currency:120"] + \
		[_("Total Tax") + ":Currency/currency:120", _("Grand Total") + ":Currency/currency:120"]

	return columns, expense_accounts, tax_accounts

def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company=%(company)s"
	if filters.get("supplier"): conditions += " and supplier = %(supplier)s"

	if filters.get("from_date"): conditions += " and posting_date>=%(from_date)s"
	if filters.get("to_date"): conditions += " and posting_date<=%(to_date)s"

	return conditions

def get_pi_invoices(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)
	data = []
	conditions = get_conditions(filters)
	data.extend( frappe.db.sql("""
		select
			name, posting_date, credit_to, supplier, supplier_name, tax_id, bill_no, bill_date,
			remarks, base_net_total, base_grand_total, outstanding_amount,
			mode_of_payment {0}
		from `tabPurchase Invoice`
		where docstatus = 1 
		and name in (select distinct parent from `tabPurchase Taxes and Charges`)
		%s
		order by posting_date desc, name desc""".format(additional_query_columns or '') % conditions, filters, as_dict=1)
	)
	return data


def get_invoice_expense_map(invoice_list):
	expense_details = frappe.db.sql("""
		select parent, expense_account, sum(base_net_amount) as amount
		from `tabPurchase Invoice Item`
		where parent in (%s)
		group by parent, expense_account
	""" % ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_expense_map = {}
	for d in expense_details:
		invoice_expense_map.setdefault(d.parent, frappe._dict()).setdefault(d.expense_account, [])
		invoice_expense_map[d.parent][d.expense_account] = flt(d.amount)

	return invoice_expense_map

def get_pi_invoice_tax_map(invoice_list, invoice_expense_map, expense_accounts):
	tax_details = frappe.db.sql("""
		select parent, account_head, case add_deduct_tax when "Add" then sum(base_tax_amount_after_discount_amount)
		else sum(base_tax_amount_after_discount_amount) * -1 end as tax_amount
		from `tabPurchase Taxes and Charges`
		where parent in (%s) and category in ('Total', 'Valuation and Total')
			and base_tax_amount_after_discount_amount != 0
		group by parent, account_head, add_deduct_tax
	""" % ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_tax_map = {}
	for d in tax_details:
		if d.account_head in expense_accounts:
			if invoice_expense_map[d.parent].has_key(d.account_head):
				invoice_expense_map[d.parent][d.account_head] += flt(d.tax_amount)
			else:
				invoice_expense_map[d.parent][d.account_head] = flt(d.tax_amount)
		else:
			invoice_tax_map.setdefault(d.parent, frappe._dict()).setdefault(d.account_head, [])
			invoice_tax_map[d.parent][d.account_head] = flt(d.tax_amount)

	return invoice_expense_map, invoice_tax_map

def get_invoice_po_pr_map(invoice_list):
	pi_items = frappe.db.sql("""
		select parent, purchase_order, purchase_receipt, po_detail, project
		from `tabPurchase Invoice Item`
		where parent in (%s) and (ifnull(purchase_order, '') != '' or ifnull(purchase_receipt, '') != '')
	""" % ', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_po_pr_map = {}
	for d in pi_items:
		if d.purchase_order:
			invoice_po_pr_map.setdefault(d.parent, frappe._dict()).setdefault(
				"purchase_order", []).append(d.purchase_order)

		pr_list = None
		if d.purchase_receipt:
			pr_list = [d.purchase_receipt]
		elif d.po_detail:
			pr_list = frappe.db.sql_list("""select distinct parent from `tabPurchase Receipt Item`
				where docstatus=1 and purchase_order_item=%s""", d.po_detail)

		if pr_list:
			invoice_po_pr_map.setdefault(d.parent, frappe._dict()).setdefault("purchase_receipt", pr_list)

		if d.project:
			invoice_po_pr_map.setdefault(d.parent, frappe._dict()).setdefault(
				"project", []).append(d.project)

	return invoice_po_pr_map

def get_account_details(invoice_list):
	account_map = {}
	accounts = list(set([inv.credit_to for inv in invoice_list]))
	for acc in frappe.db.sql("""select name, parent_account from tabAccount
		where name in (%s)""" % ", ".join(["%s"]*len(accounts)), tuple(accounts), as_dict=1):
			account_map[acc.name] = acc.parent_account

	return account_map

def get_supplier_details(suppliers):
	supplier_details = {}
	for supp in frappe.db.sql("""select name, supplier_type from `tabSupplier`
		where name in (%s)""" % ", ".join(["%s"]*len(suppliers)), tuple(suppliers), as_dict=1):
			supplier_details.setdefault(supp.name, supp.supplier_type)

	return supplier_details


#Sales Invoice 

def get_si_invoices(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	conditions = get_conditions(filters)
	a = """
		select name, posting_date, debit_to, project, customer,customer_name,po_date,po_no,owner, remarks, territory, tax_id, customer_group,
		base_net_total, base_grand_total, base_rounded_total, outstanding_amount {0}
		from `tabSales Invoice`
		where docstatus = 1 %s order by posting_date desc, name desc""".format(additional_query_columns or '') %conditions
		

	return frappe.db.sql(a, filters, as_dict=1)


def get_si_columns(invoice_list, additional_table_columns):
	income_accounts = tax_accounts = income_columns = tax_columns = []

	if invoice_list:
		income_accounts = frappe.db.sql_list("""select distinct income_account
			from `tabSales Invoice Item` where docstatus = 1 and parent in (%s)
			order by income_account""" %
			', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))

		tax_accounts = 	frappe.db.sql_list("""select distinct account_head
			from `tabSales Taxes and Charges` where parenttype = 'Sales Invoice'
			and docstatus = 1 and base_tax_amount_after_discount_amount != 0
			and parent in (%s) order by account_head""" %
			', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]))

	income_columns = [(account + ":Currency/currency:120") for account in income_accounts]
	for account in tax_accounts:
		if account not in income_accounts:
			tax_columns.append(account + ":Currency/currency:120")


	return  income_accounts, tax_accounts



def get_invoice_income_map(invoice_list):
	income_details = frappe.db.sql("""select parent, income_account, sum(base_net_amount) as amount
		from `tabSales Invoice Item` where parent in (%s) group by parent, income_account""" %
		', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_income_map = {}
	for d in income_details:
		invoice_income_map.setdefault(d.parent, frappe._dict()).setdefault(d.income_account, [])
		invoice_income_map[d.parent][d.income_account] = flt(d.amount)

	return invoice_income_map

def get_invoice_tax_map(invoice_list, invoice_income_map, income_accounts):
	tax_details = frappe.db.sql("""select parent, account_head,
		sum(base_tax_amount_after_discount_amount) as tax_amount
		from `tabSales Taxes and Charges` where parent in (%s) group by parent, account_head""" %
		', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_tax_map = {}
	for d in tax_details:
		if d.account_head in income_accounts:
			if invoice_income_map[d.parent].has_key(d.account_head):
				invoice_income_map[d.parent][d.account_head] += flt(d.tax_amount)
			else:
				invoice_income_map[d.parent][d.account_head] = flt(d.tax_amount)
		else:
			invoice_tax_map.setdefault(d.parent, frappe._dict()).setdefault(d.account_head, [])
			invoice_tax_map[d.parent][d.account_head] = flt(d.tax_amount)

	return invoice_income_map, invoice_tax_map

def get_invoice_so_dn_map(invoice_list):
	si_items = frappe.db.sql("""select parent, sales_order, delivery_note, so_detail
		from `tabSales Invoice Item` where parent in (%s)
		and (ifnull(sales_order, '') != '' or ifnull(delivery_note, '') != '')""" %
		', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_so_dn_map = {}
	for d in si_items:
		if d.sales_order:
			invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault(
				"sales_order", []).append(d.sales_order)

		delivery_note_list = None
		if d.delivery_note:
			delivery_note_list = [d.delivery_note]
		elif d.sales_order:
			delivery_note_list = frappe.db.sql_list("""select distinct parent from `tabDelivery Note Item`
				where docstatus=1 and so_detail=%s""", d.so_detail)

		if delivery_note_list:
			invoice_so_dn_map.setdefault(d.parent, frappe._dict()).setdefault("delivery_note", delivery_note_list)

	return invoice_so_dn_map

def get_invoice_cc_wh_map(invoice_list):
	si_items = frappe.db.sql("""select parent, cost_center, warehouse
		from `tabSales Invoice Item` where parent in (%s)
		and (ifnull(cost_center, '') != '' or ifnull(warehouse, '') != '')""" %
		', '.join(['%s']*len(invoice_list)), tuple([inv.name for inv in invoice_list]), as_dict=1)

	invoice_cc_wh_map = {}
	for d in si_items:
		if d.cost_center:
			invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
				"cost_center", []).append(d.cost_center)

		if d.warehouse:
			invoice_cc_wh_map.setdefault(d.parent, frappe._dict()).setdefault(
				"warehouse", []).append(d.warehouse)

	return invoice_cc_wh_map

def get_mode_of_payments(invoice_list):
	mode_of_payments = {}
	if invoice_list:
		inv_mop = frappe.db.sql("""select parent, mode_of_payment
			from `tabSales Invoice Payment` where parent in (%s) group by parent, mode_of_payment""" %
			', '.join(['%s']*len(invoice_list)), tuple(invoice_list), as_dict=1)

		for d in inv_mop:
			mode_of_payments.setdefault(d.parent, []).append(d.mode_of_payment)

	return mode_of_payments


# Journal Entry 
def get_je_invoices(filters, additional_query_columns):
	if additional_query_columns:
		additional_query_columns = ', ' + ', '.join(additional_query_columns)

	conditions = get_jv_conditions(filters)
	# ~ a = """
		# ~ select name
		# ~ base_net_total, base_grand_total, base_rounded_total, outstanding_amount {0}
		# ~ from `tabSales Invoice`
		# ~ where docstatus = 1 %s order by posting_date desc, name desc""".format(additional_query_columns or '') %conditions
		
	a = """
		select distinct 
		jv.name ,
		jva.name as jvaname,
		jv.posting_date,
		jva.party,
		"" as tax_id,
		"" as account,
		"" as mode_of_payment,
		jva.project,
		"" as bill_no,
		"" as bill_date,
		jva.journal_note,
		jv.total_debit,
		"" as dadta,
		jva.debit_in_account_currency,
		jva.credit_in_account_currency,
		jva.party_type,
		jva.party,
		jv.total_debit 
		from `tabJournal Entry Account` jva 
		left join `tabJournal Entry` jv on jv.name = jva.parent
		inner join `tabAccount`  acc on acc.name = jva.account and acc.account_type = "Tax"
		where jv.docstatus = 1 %s order by jv.posting_date desc, jv.name desc """.format(additional_query_columns or '') %conditions
		


	return frappe.db.sql(a, filters, as_dict=1)

def get_jv_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and jv.company=%(company)s"
	if filters.get("supplier"): conditions += " and jv.supplier = %(supplier)s"

	if filters.get("from_date"): conditions += " and jv.posting_date>=%(from_date)s"
	if filters.get("to_date"): conditions += " and jv.posting_date<=%(to_date)s"

	return conditions
