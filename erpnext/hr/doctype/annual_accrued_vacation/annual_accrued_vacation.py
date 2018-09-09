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
