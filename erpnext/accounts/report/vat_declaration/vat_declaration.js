// Copyright (c) 2016, Frappe Technologies Pvt. Ltd. and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["VAT Declaration"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.add_months(frappe.datetime.get_today(), -1),
			"width": "80",
			"on_change": function (query_report) {
				console.log(frappe.query_report_filters_by_name.from_date);
				query_report.report_name = 'الإقرار الضريبي من ' + frappe.query_report_filters_by_name.from_date.value
					+ " إلى " + frappe.query_report_filters_by_name.to_date.value;
			}
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"default": frappe.datetime.get_today(),
			"on_change": function (query_report) {
				console.log(frappe.query_report_filters_by_name.to_date);
				query_report.report_name = 'الإقرار الضريبي من ' + frappe.query_report_filters_by_name.from_date.value
					+ " إلى " + frappe.query_report_filters_by_name.to_date.value;
			}
		},
		{
			"fieldname":"company",
			"label": __("Company"),
			"fieldtype": "Link",
			"options": "Company",
			"default": frappe.defaults.get_user_default("Company")
		}
	],
	onload: function(report) {
		console.log(report);
	}
}
