// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt

frappe.ui.form.on('Accounting Period', {
       onload: function(frm) {
                if(frm.doc.closed_documents.length === 0 || (frm.doc.closed_documents.length === 1 && frm.doc.closed_documents[0].document_type == undefined)) {
                        frappe.call({
                                method: "get_doctypes_for_closing",
                                doc:frm.doc,
                                callback: function(r) {
                                        if(r.message) {
                                                cur_frm.clear_table("closed_documents");
                                                r.message.forEach(function(element) {
                                                        var c = frm.add_child("closed_documents");
                                                        c.document_type = element.document_type;
                                                        c.closed = element.closed;
                                                });
                                                refresh_field("closed_documents");
                                        }
                                }
                        });
                }
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
