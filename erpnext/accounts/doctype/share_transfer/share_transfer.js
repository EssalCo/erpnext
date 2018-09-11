// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Share Transfer', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.custom_date = function() {
	if(!cur_frm.doc.date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("hijri_date", r.message);

					}
				}
			})

};
