// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Accounting Period', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.custom_start_date = function() {
	if(!cur_frm.doc.start_date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.start_date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("start_hijri_date", r.message);

					}
				}
			})

};

cur_frm.cscript.custom_end_date = function() {
	if(!cur_frm.doc.end_date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.end_date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("end_hijri_date", r.message);

					}
				}
			})

};
