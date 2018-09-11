// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('GL Entry', {
	refresh: function(frm) {

	}
});

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
