# -*- coding: utf-8 -*-
# Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class AnnualAccruedVacation(Document):
	def before_insert(self):
		self.one_day_fee = self.basic_salary / self.monthly_duty_days
		self.total_balance = self.remaining_vacation_days * self.one_day_fee + self.bonus_award

		

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
