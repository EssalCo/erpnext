// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Annual Accrued Vacation', {
	refresh: function(frm) {
		if(frm.doc.docstatus === 1){
			frm.events.add_bank_entry_button(frm);
		}
	},
	setup: function (frm) {
		frm.set_query("payment_account", function () {
			var account_types = ["Bank", "Cash"];
			return {
				filters: {
					"account_type": ["in", account_types],
					"is_group": 0,
					"company": frm.doc.company
				}
			};
		}),
		frm.set_query("cost_center", function () {
			return {
				filters: {
					"is_group": 0,
					company: frm.doc.company
				}
			};
		}),
		frm.set_query("project", function () {
			return {
				filters: {
					company: frm.doc.company
				}
			};
		});
	},
	add_bank_entry_button: function(frm) {
		frappe.call({
			method: 'erpnext.hr.doctype.payroll_entry.payroll_entry.payroll_entry_has_bank_entries',
			args: {
				'name': frm.doc.name
			},
			callback: function(r) {
				if (r.message && !r.message.submitted) {
					frm.add_custom_button("Bank Entry",
						function() {
							make_bank_entry(frm);
						},
						__('Make')
					);
					frm.page.set_inner_btn_group_as_primary(__('Make'));
				}
			}
		});
	}
});

let make_bank_entry = function (frm) {
	var doc = frm.doc;
	if (doc.company && doc.year_start_date && doc.year_end_date) {
		return frappe.call({
			doc: cur_frm.doc,
			method: "make_payment_entry",
			callback: function (r) {
				if (r.message)
					var doc = frappe.model.sync(r.message)[0];
				frappe.set_route("Form", doc.doctype, doc.name);
			}
		});
	} else {
		frappe.msgprint(__("Company, From Date and To Date is mandatory"));
	}
};
