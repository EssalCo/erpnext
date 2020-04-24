from __future__ import unicode_literals

import frappe
from frappe import _


def execute(filters=None):
	if not filters: filters = dict()
	columns = get_columns()
	data = get_data(filters)
	return columns, data


def get_columns():
	# return columns

	return [
		"{label}:{type}:{width}".format(label=" ", type="Data", width=160),
		"{label}:{type}:{width}".format(label=_("Balance", "ar"), type="Data", width=240),
		"{label}:{type}:{width}".format(label=_("Modification", "ar"), type="Data", width=240),
		"{label}:{type}:{width}".format(label=_("VAT", "ar"), type="Data", width=240)
	]


def get_data(filters):
	conditions = get_conditions(filters)

	result = [
		[
			"<b>" + _("VAT", "ar") + "</b>",
			"<b>" + _("Sales", "ar") + "</b>",
			"<b>" + _("Modification", "ar") + "</b>",
			"<b>" + _("VAT", "ar") + "</b>"
		]
	]

	currency = frappe.get_value("Company", filters.get("company"), "default_currency")
	sales_amounts = frappe.db.sql("""SELECT 
    COALESCE(SUM(base_net_amount), 0) AS amount
FROM
    `tabSales Invoice Item`
WHERE
    parent IN (SELECT 
            name
        FROM
            `tabSales Invoice`
        WHERE
            docstatus = 1 {conditions}) 
UNION SELECT 
    COALESCE(SUM(base_tax_amount_after_discount_amount), 0) AS amount
FROM
    `tabSales Taxes and Charges`
WHERE
    parent IN (SELECT 
            name
        FROM
            `tabSales Invoice`
        WHERE
            docstatus = 1 {conditions});""".format(
		conditions=conditions
	), as_dict=True)

	if len(sales_amounts) == 0:
		sales_amounts = [
			dict(
				amount=0
			),
			dict(
				amount=0
			)
		]
	if len(sales_amounts) == 1:
		sales_amounts += [
			dict(
				amount=0
			)
		]
	result.append([
		"<b>" + "VAT" + "</b>",
		sales_amounts[0]['amount'],
		"-0.0",
		sales_amounts[1]['amount']
	])

	result.append([
		"<b>" + _("Zero VAT", "ar") + "</b>",
		"0.0", "-0.0", "0.0"
	])

	result.append([
		"<b>" + _("Free VAT", "ar") + "</b>",
		"0.0", "-0.0", "0.0"
	])

	result.append([
		"<b>" + _("Total", "ar") + "</b>",
		"<b>" + "{0} {1}".format(
			sales_amounts[0]['amount'], _(currency or "SAR", "ar")) + "</b>",
		"<b>" + "-0.0" + "</b>",
		"<b>" + "{0} {1}".format(sales_amounts[1]['amount'], _(currency or "SAR", "ar")) + "</b>"
	])

	result.append([
		" ", " ", " ", " "
	])

	purchases_amounts = frappe.db.sql("""SELECT 
    COALESCE(SUM(base_net_amount), 0) AS amount
FROM
    `tabPurchase Invoice Item`
WHERE
    parent IN (SELECT 
            name
        FROM
            `tabPurchase Invoice`
        WHERE
            docstatus = 1 {conditions}) 
UNION SELECT 
    COALESCE(CASE add_deduct_tax
                WHEN 'Add' THEN SUM(base_tax_amount_after_discount_amount)
                ELSE SUM(base_tax_amount_after_discount_amount) * - 1
            END,
            0) AS amount
FROM
    `tabPurchase Taxes and Charges`
WHERE
    parent IN (SELECT 
            name
        FROM
            `tabPurchase Invoice`
        WHERE
            docstatus = 1 {conditions})
        AND category IN ('Total' , 'Valuation and Total')
        AND base_tax_amount_after_discount_amount != 0;""".format(
		conditions=conditions
	), as_dict=True)

	if len(purchases_amounts) == 0:
		purchases_amounts = [
			dict(
				amount=0
			),
			dict(
				amount=0
			)
		]
	if len(purchases_amounts) == 1:
		purchases_amounts += [
			dict(
				amount=0
			)
		]
	result.append([
		"<b>" + _("VAT", "ar") + "</b>",
		"<b>" + _("Purchases", "ar") + "</b>",
		"<b>" + _("Modification", "ar") + "</b>",
		"<b>" + _("Paid VAT", "ar") + "</b>"
	])

	result.append([
		"<b>" + _("VAT", "ar") + "</b>",
		purchases_amounts[0]['amount'],
		"-0.0",
		purchases_amounts[1]['amount']
	])

	result.append([
		"<b>" + _("Zero VAT", "ar") + "</b>", "0.0", "-0.0", "0.0"
	])

	result.append([
		"<b>" + _("Free VAT", "ar") + "</b>",
		"0.0", "-0.0", "0.0"
	])

	result.append([
		"<b>" + _("Total", "ar") + "</b>",
		"<b>" + "{0} {1}".format(
			purchases_amounts[0]['amount'], _(currency or "SAR", "ar")) + "</b>",
		"<b>" + "-0.0" + "</b>",
		"<b>" + "{0} {1}".format(purchases_amounts[1]['amount'], _(currency or "SAR", "ar")) + "</b>"
	])

	return result


def get_conditions(filters):
	conditions = ""

	if filters.get("company"): conditions += " and company = '{0}'".format(filters["company"])

	if filters.get("from_date"): conditions += " and posting_date >= '{0}'".format(filters["from_date"])
	if filters.get("to_date"): conditions += " and posting_date <= '{0}'".format(filters["to_date"])

	return conditions
