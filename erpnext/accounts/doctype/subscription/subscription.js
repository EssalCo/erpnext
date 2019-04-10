// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Subscription', {
	refresh: function(frm) {
		if(!frm.is_new()){
			if(frm.doc.status !== 'Cancelled'){
				frm.add_custom_button(
					__('Cancel Subscription'),
					() => frm.events.cancel_this_subscription(frm)
				);
				frm.add_custom_button(
					__('Fetch Subscription Updates'),
					() => frm.events.get_subscription_updates(frm)
				);
			}
			else if(frm.doc.status === 'Cancelled'){
				frm.add_custom_button(
					__('Restart Subscription'),
					() => frm.events.renew_this_subscription(frm)
				);
			}
		}
	},

	cancel_this_subscription: function(frm) {
		const doc = frm.doc;
		frappe.confirm(
			__('This action will stop future billing. Are you sure you want to cancel this subscription?'),
			function() {
				frappe.call({
					method:
					"erpnext.accounts.doctype.subscription.subscription.cancel_subscription",
					args: {name: doc.name},
					callback: function(data){
						if(!data.exc){
							frm.reload_doc();
						}
					}
				});
			}
		);
	},

	renew_this_subscription: function(frm) {
		const doc = frm.doc;
		frappe.confirm(
			__('You will lose records of previously generated invoices. Are you sure you want to restart this subscription?'),
			function() {
				frappe.call({
					method:
					"erpnext.accounts.doctype.subscription.subscription.restart_subscription",
					args: {name: doc.name},
					callback: function(data){
						if(!data.exc){
							frm.reload_doc();
						}
					}
				});
			}
		);
	},

	get_subscription_updates: function(frm) {
		const doc = frm.doc;
		frappe.call({
			method:
			"erpnext.accounts.doctype.subscription.subscription.get_subscription_updates",
			args: {name: doc.name},
			freeze: true,
			callback: function(data){
				if(!data.exc){
					frm.reload_doc();
				}
			}
		});
	}
});
<<<<<<< HEAD

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
=======
>>>>>>> b0c939d280fc519f43ce595618a6b68e5daf2be7
