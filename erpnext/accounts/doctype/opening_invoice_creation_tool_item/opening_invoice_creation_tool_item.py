# -*- coding: utf-8 -*-
# Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from erpnext.utilities.hijri_date import convert_to_hijri

class OpeningInvoiceCreationToolItem(Document):
	def before_save(self):
		self.posting_hijri_date = convert_to_hijri(self.posting_date)
		self.due_hijri_date = convert_to_hijri(self.due_date)
