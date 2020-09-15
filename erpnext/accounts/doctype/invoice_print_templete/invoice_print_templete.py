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
        self.vat = self.total * 15 / 115.0
        self.total = self.total_without_vat + self.vat

    def before_insert(self):
        for record in self.records:
            record.total = record.value * record.count
        self.total_without_vat = sum(temp.total for temp in self.records)
        self.vat = self.total_without_vat * 0.15
        self.total = self.total_without_vat + self.vat
        self.invoice_id = frappe.db.count(
            "Invoice Print Templete",
            dict(
                company=self.company
            )
        ) + 1
