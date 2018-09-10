# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from frappe.model.document import Document
from erpnext.utilities.hijri_date import convert_to_hijri


class PaymentSchedule(Document):
	def before_save(self):
		self.due_hijri_date = convert_to_hijri(self.due_date)
