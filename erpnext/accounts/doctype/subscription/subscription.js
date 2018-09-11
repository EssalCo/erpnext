// Copyright (c) 2017, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subscription', {
	setup: function(frm) {
		frm.fields_dict['reference_doctype'].get_query = function(doc) {
			return {
				query: "erpnext.accounts.doctype.subscription.subscription.subscription_doctype_query"
			};
		};

		frm.fields_dict['reference_document'].get_query = function() {
			return {
				filters: {
					"docstatus": 1,
					"subscription": ''
				}
			};
		};

		frm.fields_dict['print_format'].get_query = function() {
			return {
				filters: {
					"doc_type": frm.doc.reference_doctype
				}
			};
		};
	},

	refresh: function(frm) {
		if(frm.doc.docstatus == 1) {
			let label = __('View {0}', [frm.doc.reference_doctype]);
			frm.add_custom_button(__(label),
				function() {
					frappe.route_options = {
						"subscription": frm.doc.name,
					};
					frappe.set_route("List", frm.doc.reference_doctype);
				}
			);

			if(frm.doc.status != 'Stopped') {
				frm.add_custom_button(__("Stop"),
					function() {
						frm.events.stop_resume_subscription(frm, "Stopped");
					}
				);
			}

			if(frm.doc.status == 'Stopped') {
				frm.add_custom_button(__("Resume"),
					function() {
						frm.events.stop_resume_subscription(frm, "Resumed");
					}
				);
			}
		}
	},

	stop_resume_subscription: function(frm, status) {
		frappe.call({
			method: "erpnext.accounts.doctype.subscription.subscription.stop_resume_subscription",
			args: {
				subscription: frm.doc.name,
				status: status
			},
			callback: function(r) {
				if(r.message) {
					frm.set_value("status", r.message);
					frm.reload_doc();
				}
			}
		});
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

cur_frm.cscript.custom_next_schedule_date = function() {
	if(!cur_frm.doc.next_schedule_date){
		return
	}
	frappe.call({
				method: "erpnext.utilities.hijri_date.convert_to_hijri",
				args:{
					date:cur_frm.doc.next_schedule_date
				},
				callback: function (r) {
					if (r.message) {
						cur_frm.set_value("next_schedule_date", r.message);

					}
				}
			})

};
