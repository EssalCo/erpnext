// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

<<<<<<< HEAD
frappe.require("assets/erpnext/js/financial_statements.js", function () {
    frappe.query_reports["Trial Balance"] = {
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
                "fieldname": "fiscal_year",
                "label": __("Fiscal Year"),
                "fieldtype": "Link",
                "options": "Fiscal Year",
                "default": frappe.defaults.get_user_default("fiscal_year"),
                "reqd": 1,
                "on_change": function (query_report) {
                    var fiscal_year = query_report.get_values().fiscal_year;
                    if (!fiscal_year) {
                        return;
                    }
                    frappe.model.with_doc("Fiscal Year", fiscal_year, function (r) {
                        var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
                        frappe.query_report_filters_by_name.from_date.set_input(fy.year_start_date);
                        frappe.query_report_filters_by_name.to_date.set_input(fy.year_end_date);
                        query_report.trigger_refresh();
                    });
                }
            },
            {
                "fieldname": "from_date",
                "label": __("From Date"),
                "fieldtype": "Date",
                "default": frappe.defaults.get_user_default("year_start_date"),
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
                "default": frappe.defaults.get_user_default("year_end_date"),
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
                "fieldname": "with_period_closing_entry",
                "label": __("Period Closing Entry"),
                "fieldtype": "Check",
                "default": 1
            },
            {
                "fieldname": "show_zero_values",
                "label": __("Show zero values"),
                "fieldtype": "Check"
            },
            {
                "fieldname": "show_unclosed_fy_pl_balances",
                "label": __("Show unclosed fiscal year's P&L balances"),
                "fieldtype": "Check"
            }
        ],
        "formatter": erpnext.financial_statements.formatter,
        "tree": true,
        "name_field": "account",
        "parent_field": "parent_account",
        "initial_depth": 3
    }
=======
frappe.require("assets/erpnext/js/financial_statements.js", function() {
	frappe.query_reports["Trial Balance"] = {
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
				"fieldname": "fiscal_year",
				"label": __("Fiscal Year"),
				"fieldtype": "Link",
				"options": "Fiscal Year",
				"default": frappe.defaults.get_user_default("fiscal_year"),
				"reqd": 1,
				"on_change": function(query_report) {
					var fiscal_year = query_report.get_values().fiscal_year;
					if (!fiscal_year) {
						return;
					}
					frappe.model.with_doc("Fiscal Year", fiscal_year, function(r) {
						var fy = frappe.model.get_doc("Fiscal Year", fiscal_year);
						frappe.query_report.set_filter_value({
							from_date: fy.year_start_date,
							to_date: fy.year_end_date
						});
					});
				}
			},
			{
				"fieldname": "from_date",
				"label": __("From Date"),
				"fieldtype": "Date",
				"default": frappe.defaults.get_user_default("year_start_date"),
			},
			{
				"fieldname": "to_date",
				"label": __("To Date"),
				"fieldtype": "Date",
				"default": frappe.defaults.get_user_default("year_end_date"),
			},
			{
				"fieldname":"cost_center",
				"label": __("Cost Center"),
				"fieldtype": "Link",
				"options": "Cost Center",
				"get_query": function() {
					var company = frappe.query_report.get_filter_value('company');
					return {
						"doctype": "Cost Center",
						"filters": {
							"company": company,
						}
					}
				}
			},
			{
				"fieldname":"finance_book",
				"label": __("Finance Book"),
				"fieldtype": "Link",
				"options": "Finance Book",
			},
			{
				"fieldname": "with_period_closing_entry",
				"label": __("Period Closing Entry"),
				"fieldtype": "Check",
				"default": 1
			},
			{
				"fieldname": "show_zero_values",
				"label": __("Show zero values"),
				"fieldtype": "Check"
			},
			{
				"fieldname": "show_unclosed_fy_pl_balances",
				"label": __("Show unclosed fiscal year's P&L balances"),
				"fieldtype": "Check"
			},
			{
				"fieldname": "include_default_book_entries",
				"label": __("Include Default Book Entries"),
				"fieldtype": "Check"
			}
		],
		"formatter": erpnext.financial_statements.formatter,
		"tree": true,
		"name_field": "account",
		"parent_field": "parent_account",
		"initial_depth": 3
	}
>>>>>>> b0c939d280fc519f43ce595618a6b68e5daf2be7
});

