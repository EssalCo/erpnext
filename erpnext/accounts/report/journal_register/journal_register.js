// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Journal Register"] = {
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
            "fieldname": "from_date",
            "label": __("From Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
            "reqd": 1,
            "width": "60px"
        },
        {
            "fieldname": "to_date",
            "label": __("To Date"),
            "fieldtype": "Date",
            "default": frappe.datetime.get_today(),
            "reqd": 1,
            "width": "60px"
        },
        {
            "fieldname": "account",
            "label": __("Account"),
            "fieldtype": "Link",
            "options": "Account",
            "get_query": function () {
                var company = frappe.query_report.get_filter_value('company');
                return {
                    "doctype": "Account",
                    "filters": {
                        "company": company,
                    }
                }
            }
        },
        {
            "fieldname": "voucher_no",
            "label": __("Voucher No"),
            "fieldtype": "Data",
        },
        {
            "fieldname": "cost_center",
            "label": __("Cost Center"),
            "fieldtype": "Link",
            "options": "Cost Center"
            // "fieldtype": "MultiSelect",
            // get_data: function () {
            // 	var cost_centers = frappe.query_report.get_filter_value("cost_center") || "";
            //
            // 	const values = cost_centers.split(/\s*,\s*/).filter(d => d);
            // 	const txt = cost_centers.match(/[^,\s*]*$/)[0] || '';
            // 	let data = [];
            //
            // 	frappe.call({
            // 		type: "GET",
            // 		method: 'frappe.desk.search.search_link',
            // 		async: false,
            // 		no_spinner: true,
            // 		args: {
            // 			doctype: "Cost Center",
            // 			txt: txt,
            // 			filters: {
            // 				"company": frappe.query_report.get_filter_value("company"),
            // 				"name": ["not in", values]
            // 			}
            // 		},
            // 		callback: function (r) {
            // 			data = r.results;
            // 		}
            // 	});
            // 	return data;
            // }
        },
        {
            "fieldname": "project",
            "label": __("Project"),
            "options": "Project",
            "fieldtype": "Link",
            // "fieldtype": "MultiSelect",
            // get_data: function () {
            // 	var projects = frappe.query_report.get_filter_value("project") || "";
            //
            // 	const values = projects.split(/\s*,\s*/).filter(d => d);
            // 	const txt = projects.match(/[^,\s*]*$/)[0] || '';
            // 	let data = [];
            //
            // 	frappe.call({
            // 		type: "GET",
            // 		method: 'frappe.desk.search.search_link',
            // 		async: false,
            // 		no_spinner: true,
            // 		args: {
            // 			doctype: "Project",
            // 			txt: txt,
            // 			filters: {
            // 				"name": ["not in", values]
            // 			}
            // 		},
            // 		callback: function (r) {
            // 			data = r.results;
            // 		}
            // 	});
            // 	return data;
            // }
        },
        {
            "fieldtype": "Break",
        },
    ]
};
