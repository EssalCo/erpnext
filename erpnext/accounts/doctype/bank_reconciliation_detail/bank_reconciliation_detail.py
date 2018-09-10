# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
# License: GNU General Public License v3. See license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.utilities.hijri_date import convert_to_hijri

class BankReconciliationDetail(Document):
	def before_save(self):
		self.posting_hijri_date = convert_to_hijri(self.posting_date)
		self.cheque_hijri_date = convert_to_hijri(self.cheque_date)
		self.clearance_hijri_date = convert_to_hijri(self.clearance_date)