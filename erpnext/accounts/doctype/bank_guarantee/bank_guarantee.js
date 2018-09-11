// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Bank Guarantee', {
	refresh: function(frm) {
		cur_frm.set_query("account", function() {
			return {
				"filters": {
					"account_type": "Bank",
					"is_group": 0
				}
			};
		});
		cur_frm.set_query("project", function() {
			return {
				"filters": {
					"customer": cur_frm.doc.customer
				}
			};
		});
	},
	start_date: function(frm) {
		var end_date = frappe.datetime.add_days(cur_frm.doc.start_date, cur_frm.doc.validity - 1);
		cur_frm.set_value("end_date", end_date);
	},
	validity: function(frm) {
		var end_date = frappe.datetime.add_days(cur_frm.doc.start_date, cur_frm.doc.validity - 1);
		cur_frm.set_value("end_date", end_date);
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