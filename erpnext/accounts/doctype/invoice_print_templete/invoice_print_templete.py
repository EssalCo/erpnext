# -*- coding: utf-8 -*-
# Copyright (c) 2019, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class InvoicePrintTemplete(Document):
                def before_save(self):
                    for record in self.records:
                        record.total = record.value * record.count
                    self.total_without_vat = sum(temp.total for temp in self.records)
                    self.vat = self.total * 5 / 105.0
                    self.total = self.total_without_vat + self.vat
                
                def before_insert(self):
                    for record in self.records:
                        record.total = record.value * record.count
                    self.total_without_vat = sum(temp.total for temp in self.records)
                    self.vat = self.total * 5 / 105.0
                    self.total = self.total_without_vat + self.vat
