# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe import _, msgprint


class AnnualAccruedVacation(Document):
	def before_insert(self):
		self.one_day_fee = self.basic_salary / self.monthly_duty_days
		self.total_balance = self.remaining_vacation_days * self.one_day_fee + self.bonus_award
		if not self.payment_account:
            		msgprint(
				_("Please set Payment Account"),
				title="Error", indicator="red"
			    )
	
	def get_default_payroll_payable_account(self):
		payroll_payable_account = frappe.db.get_value("Company",
			{"company_name": self.company}, "default_payroll_payable_account")
		if not payroll_payable_account:
			frappe.throw(_("Please set Default Payment Account"))

		return payroll_payable_account
	
	def make_payment_entry(self):
		self.check_permission('write')

		default_payroll_payable_account = self.get_default_payroll_payable_account()
		precision = frappe.get_precision("Journal Entry Account", "debit_in_account_currency")

		if self.total_balance:
		    journal_entry = frappe.new_doc('Journal Entry')
		    journal_entry.voucher_type = 'Bank Entry'
		    journal_entry.user_remark = _('Payment of accrued vacation from {0} to {1}') \
			.format(self.year_start_date, self.year_end_date)
		    journal_entry.company = self.company
		    journal_entry.posting_date = self.creation

		    payment_amount = flt(self.total_balance, precision)

		    journal_entry.set("accounts", [
			{
			    "account": self.payment_account,
			    "credit_in_account_currency": payment_amount
			},
			{
			    "account": default_payroll_payable_account,
			    "debit_in_account_currency": payment_amount,
			    "reference_type": self.doctype,
			    "reference_name": self.name
			}
		    ])
		    return journal_entry.as_dict()
		else:
		    msgprint(
			_("There are no Credit for the employee to process."),
			title="Error", indicator="red"
		    )
		

def get_accrued_vacation_bank_entries(accrued_vacation_name):
	journal_entries = frappe.db.sql(
		'select name from `tabJournal Entry Account` '
		'where reference_type="Employee Advance" '
		'and reference_name=%s and docstatus=1',
		accrued_vacation_name,
		as_dict=1
	)

	return journal_entries


@frappe.whitelist()
def accrued_vacation_has_bank_entries(name):
	response = dict()

	bank_entries = get_accrued_vacation_bank_entries(name)
	response['submitted'] = 1 if bank_entries else 0

	return response
