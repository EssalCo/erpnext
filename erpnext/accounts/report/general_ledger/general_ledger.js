// Copyright (c) 2018, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.query_reports["General Ledger"] = {
    "filters": [
        {
            "fieldname": "company",
            "label": __("Company"),
            "fieldtype": "Link",
            "options": "Company",
            "default": frappe.defaults.get_user_default("Company"),
            "reqd": 1
        },
        {
            "fieldname": "finance_book",
            "label": __("Finance Book"),
            "fieldtype": "Link",
            "options": "Finance Book"
        },
        {
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1,
            "width": "60px",
            on_change: function () {
                let from_date_var = frappe.query_report_filters_by_name.from_date.get_value();
                if (!from_date_var) {
                    return
                }
                frappe.call({
                    method: "erpnext.utilities.hijri_date.convert_to_hijri",
                    args: {
                        date: from_date_var
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.query_report_filters_by_name.from_date_hijri.set_value(r.message)
                        }
                    }
                })
            }
        },
        {
            "fieldname": "from_date_hijri",
            "label": __("From Date Hijri"),
            "fieldtype": "Data",
            "read_only": 1,
            "width": "60px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1,
            "width": "60px",
            on_change: function () {
                let to_date_var = frappe.query_report_filters_by_name.to_date.get_value();
                if (!to_date_var) {
                    return
                }
                frappe.call({
                    method: "erpnext.utilities.hijri_date.convert_to_hijri",
                    args: {
                        date: to_date_var
                    },
                    callback: function (r) {
                        if (r.message) {
                            frappe.query_report_filters_by_name.to_date_hijri.set_value(r.message)

                        }
                    }
                })
            }
        },
        {
            "fieldname": "to_date_hijri",
            "label": __("To Date Hijri"),
            "fieldtype": "Data",
            "read_only": 1,
            "width": "60px"
        },
        {
            "fieldname": "account",
            "label": __("Account"),
            "fieldtype": "Link",
            "options": "Account",
            "get_query": function () {
                var company = frappe.query_report_filters_by_name.company.get_value();
                return {
                    "doctype": "Account",
                    "filters": {
                        "company": company,
                    }
                }
            }
            // "get_query": function() {
            // 	var company = frappe.query_report.get_filter_value('company');
            // 	return {
            // 		"doctype": "Account",
            // 		"filters": {
            // 			"company": company,
            // 		}
            // 	}
            // }
        },
        {
            "fieldname": "voucher_no",
            "label": __("Voucher No"),
            "fieldtype": "Data",
            // on_change: function() {
            // 	frappe.query_report.set_filter_value('group_by', "");
            // }
        },
        {
            "fieldname": "party_type",
            "label": __("Party Type"),
            "fieldtype": "Link",
            "options": "Party Type",
            "default": "",
            on_change: function () {
                frappe.query_report_filters_by_name.party.set_value("");
            }
        },
        {
            "fieldname": "party",
            "label": __("Party"),
            "fieldtype": "Dynamic Link",
            "get_options": function () {
                var party_type = frappe.query_report_filters_by_name.party_type.get_value();
                var party = frappe.query_report_filters_by_name.party.get_value();
                if (party && !party_type) {
                    frappe.throw(__("Please select Party Type first"));
                }
                return party_type;
            },
            on_change: function () {
                var party_type = frappe.query_report_filters_by_name.party_type.get_value();
                var party = frappe.query_report_filters_by_name.party.get_value();
                if (!party_type || !party) {
                    frappe.query_report_filters_by_name.party_name.set_value("");
                    return;
                }
                var fieldname = erpnext.utils.get_party_name(party_type) || "name";
                frappe.db.get_value(party_type, party, fieldname, function (value) {
                    frappe.query_report_filters_by_name.party_name.set_value(value[fieldname]);
                });

                if (party_type === "Customer" || party_type === "Supplier") {
                    frappe.db.get_value(party_type, party, "tax_id", function (value) {
                        frappe.query_report_filters_by_name.tax_id.set_value(value["tax_id"]);
                    });
                }
            }
        },
        // get_data: function(txt) {
        // 	if (!frappe.query_report.filters) return;
        //
        // 	let party_type = frappe.query_report.get_filter_value('party_type');
        // 	if (!party_type) return;
        //
        // 	return frappe.db.get_link_options(party_type, txt);
        // },
        // on_change: function() {
        // 	var party_type = frappe.query_report.get_filter_value('party_type');
        // 	var parties = frappe.query_report.get_filter_value('party');
        //
        // 	if(!party_type || parties.length === 0 || parties.length > 1) {
        // 		frappe.query_report.set_filter_value('party_name', "");
        // 		frappe.query_report.set_filter_value('tax_id', "");
        // 		return;
        // 	} else {
        // 		var party = parties[0];
        // 		var fieldname = erpnext.utils.get_party_name(party_type) || "name";
        // 		frappe.db.get_value(party_type, party, fieldname, function(value) {
        // 			frappe.query_report.set_filter_value('party_name', value[fieldname]);
        // 		});
        //
        // 		if (party_type === "Customer" || party_type === "Supplier") {
        // 			frappe.db.get_value(party_type, party, "tax_id", function(value) {
        // 				frappe.query_report.set_filter_value('tax_id', value["tax_id"]);
        // 			});
        // 		}
        // 	}
        // }
        {
            "fieldname": "party_name",
            "label": __("Party Name"),
            "fieldtype": "Data",
            "hidden": 1
        },
        {
            "fieldname": "group_by",
            "label": __("Group by"),
            "fieldtype": "Select",
            "options": ["", __("Group by Voucher"), __("Group by Voucher (Consolidated)"),
                __("Group by Account"), __("Group by Party"), __("No Grouping (Consolidated)")],
            "default": __("Group by Voucher (Consolidated)")
        },
        {
            "fieldname": "tax_id",
            "label": __("Tax Id"),
            "fieldtype": "Data",
            "hidden": 1
        },
        // {
        // 	"fieldname": "presentation_currency",
        // 	"label": __("Currency"),
        // 	"fieldtype": "Select",
        // 	"options": "Currency"
        // },
        // {
        //     "fieldname": "cost_center",
        //     "label": __("Cost Center"),
        //     "fieldtype": "Link",
        //     "options": "Cost Center"
        //     // "fieldtype": "MultiSelectList",
        //     // get_data: function(txt) {
        //     // 	return frappe.db.get_link_options('Cost Center', txt);
        //     // }
        // },
        {
            "fieldname": "project",
            "label": __("Project"),
            "fieldtype": "Link",
            "options": "Project"
            // "fieldtype": "MultiSelectList",
            // get_data: function(txt) {
            // 	return frappe.db.get_link_options('Project', txt);
            // }
        },
        {
            "fieldname": "show_opening_entries",
            "label": __("Show Opening Entries"),
            "fieldtype": "Check"
        },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center",
            "get_query": function () {
                var company = frappe.query_report_filters_by_name.company.get_value();
                return {
                    "doctype": "Cost Center",
                    "filters": {
                        "company": company,
                    }
                }
            }
            // "get_query": function() {
            // 	var company = frappe.query_report.get_filter_value('company');
            // 	return {
            // 		"doctype": "Account",
            // 		"filters": {
            // 			"company": company,
            // 		}
            // 	}
            // }
        },
        {
            "fieldname": "customize_party_text",
            "label": __("Customize Party Text"),
            "fieldtype": "Check"
        },
    ]
};

// let dimension_filters = erpnext.get_dimension_filters();
//
// dimension_filters.then((dimensions) => {
// 	dimensions.forEach((dimension) => {
// 		frappe.query_reports["General Ledger"].filters.splice(15, 0 ,{
// 			"fieldname": dimension["fieldname"],
// 			"label": __(dimension["label"]),
// 			"fieldtype": "Link",
// 			"options": dimension["document_type"]
// 		});
// 	});
// });

