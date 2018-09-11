// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Accounts Settings', {
	refresh: function(frm) {

	}
});

cur_frm.cscript.custom_acc_frozen_upto = function() {
	if(!cur_frm.doc.acc_frozen_upto){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.acc_frozen_upto
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("accounts_frozen_hijri_date", r.message);

					}
				}
			})

};
