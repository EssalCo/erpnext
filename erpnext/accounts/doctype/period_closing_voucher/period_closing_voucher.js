// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.ui.form.on('Period Closing Voucher', {
	onload: function(frm) {
		if (!frm.doc.transaction_date) frm.doc.transaction_date = frappe.datetime.obj_to_str(new Date());
	},
	
	setup: function(frm) {
		frm.set_query("closing_account_head", function() {
			return {
				filters: [
					['Account', 'company', '=', frm.doc.company],
					['Account', 'is_group', '=', '0'],
					['Account', 'freeze_account', '=', 'No'],
					['Account', 'root_type', 'in', 'Liability, Equity']
				]
			}
		});
	},
	
	refresh: function(frm) {
		if(frm.doc.docstatus==1) {
			frm.add_custom_button(__('Ledger'), function() {
				frappe.route_options = {
					"voucher_no": frm.doc.name,
					"from_date": frm.doc.posting_date,
					"to_date": frm.doc.posting_date,
					"company": frm.doc.company,
					group_by_voucher: 0
				};
				frappe.set_route("query-report", "General Ledger");
			}, "fa fa-table");
		}
	}
	
})


cur_frm.cscript.custom_transaction_date = function() {
	if(!cur_frm.doc.transaction_date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.transaction_date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("transaction_hijri_date", r.message);

					}
				}
			})

};

cur_frm.cscript.custom_posting_date = function() {
	if(!cur_frm.doc.posting_date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.posting_date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("posting_hijri_date", r.message);

					}
				}
			})

};
