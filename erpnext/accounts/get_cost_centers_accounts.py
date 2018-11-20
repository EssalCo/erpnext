# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import erpnext
import frappe
from erpnext.accounts.report.financial_statements \
    import filter_accounts, set_gl_entries_by_account, filter_out_zero_value_rows
from frappe import _
from frappe.utils import flt, getdate, formatdate, cstr


@frappe.whitelist(allow_guest=True)
def get_cost_centers_accounts():
    # 'cost_center',
    # 'company_name'
    # 'fiscal_year'
    # 'to_date'
    # 'from_date'

    try:
        data = frappe.form_dict

        cost_center = data.get('cost_center')
        company_name = data.get('company_name')
        from_date = data.get('from_date')
        to_date = data.get('to_date')
        fiscal_year = data.get('fiscal_year')

        frappe.set_user("Administrator")

        company = frappe.get_value("Company", company_name, "name")

        if not company:
            return dict(status=False, message="{0} is not an existing company".format(company_name))

        cost_center_company = frappe.get_value("Cost Center", cost_center, "company")

        if cost_center_company != company_name:
            return dict(status=False, message="This cost center does not belong to {0}".format(company_name))
        
        budgets = [temp.account for temp in frappe.get_list(
            "Budget Account",
            fields=["name"],
            filters=dict(
                cost_center=cost_center
            ),
            ignore_permissions=True,
            ignore_ifnull=True)]
        budget_accounts = [temp.account for temp in frappe.get_list(
            "Budget Account",
            fields=["account", "budget_amount"],
            filters=dict(
                parent=("in", budgets)
            ),
            ignore_permissions=True,
            ignore_ifnull=True)]

        filters = dict(
            company=company_name,
            from_date=from_date,
            to_date=to_date,
            fiscal_year=fiscal_year,
            show_zero_values=True
        )
        data = get_data(filters)

        accounts = list()
        for d in data:
            if d.get("account"):
                if d['account'] in budget_accounts:
                    accounts.append(d)

    except Exception as e:
        return dict(status=False, message=str(e))
    return dict(status=True, message="Success", accounts=accounts or budget_accounts)


value_fields = ("opening_debit", "opening_credit", "debit", "credit", "closing_debit", "closing_credit")


def validate_filters(filters):
    if not filters.get("fiscal_year"):
        frappe.throw(_("Fiscal Year {0} is required").format(filters.get("fiscal_year")))

    fiscal_year = frappe.db.get_value(
        "Fiscal Year",
        filters.get("fiscal_year"),
        ["year_start_date", "year_end_date"],
        as_dict=True
    )
    if not fiscal_year:
        frappe.throw(_("Fiscal Year {0} does not exist").format(filters.get("fiscal_year")))
    else:
        filters["year_start_date"] = getdate(fiscal_year.year_start_date)
        filters["year_end_date"] = getdate(fiscal_year.year_end_date)

    if not filters.get("from_date"):
        filters["from_date"] = filters.get("year_start_date")

    if not filters.get("to_date"):
        filters["to_date"] = filters.get("year_end_date")

    filters["from_date"] = getdate(filters.get("from_date"))
    filters["to_date"] = getdate(filters.get("to_date"))

    if filters.get("from_date") > filters.get("to_date"):
        frappe.throw(_("From Date cannot be greater than To Date"))

    if (filters.get("from_date") < filters.get("year_start_date")) or (
                filters.get("from_date") > filters.get("year_end_date")):
        frappe.msgprint(_("From Date should be within the Fiscal Year. Assuming From Date = {0}") \
                        .format(formatdate(filters.year_start_date)))

        filters["from_date"] = filters.get("year_start_date")

    if (filters.get("to_date") < filters.get("year_start_date")) or (
                filters.get("to_date") > filters.get("year_end_date")):
        frappe.msgprint(_("To Date should be within the Fiscal Year. Assuming To Date = {0}") \
                        .format(formatdate(filters.get("year_end_date"))))
        filters["to_date"] = filters.get("year_end_date")


def get_data(filters):
    accounts = frappe.db.sql("""SELECT 
    name,
    parent_account,
    account_name,
    root_type,
    report_type,
    lft,
    rgt
FROM
    `tabAccount`
WHERE
    company = %s
ORDER BY lft;""", filters.get("company"), as_dict=True)
    company_currency = erpnext.get_company_currency(filters.get("company"))

    if not accounts:
        return None

    accounts, accounts_by_name, parent_children_map = filter_accounts(accounts)

    min_lft, max_rgt = frappe.db.sql("""SELECT 
    MIN(lft), MAX(rgt)
FROM
    `tabAccount`
WHERE
    company = %s;""", (filters.get("company"),))[0]

    gl_entries_by_account = {}

    set_gl_entries_by_account(
        filters.get("company"),
        filters.get("from_date"),
        filters.get("to_date"),
        min_lft,
        max_rgt,
        filters,
        gl_entries_by_account,
        ignore_closing_entries=False)

    opening_balances = get_opening_balances(filters)

    total_row = calculate_values(
        accounts,
        gl_entries_by_account,
        opening_balances,
        filters,
        company_currency)
    accumulate_values_into_parents(accounts, accounts_by_name)

    data = prepare_data(accounts, filters, total_row, parent_children_map, company_currency)
    data = filter_out_zero_value_rows(
        data,
        parent_children_map,
        show_zero_values=True)

    return data


def get_opening_balances(filters):
    balance_sheet_opening = get_rootwise_opening_balances(filters, "Balance Sheet")
    pl_opening = get_rootwise_opening_balances(filters, "Profit and Loss")

    balance_sheet_opening.update(pl_opening)
    return balance_sheet_opening


def get_rootwise_opening_balances(filters, report_type):
    additional_conditions = ""
    # additional_conditions = " and posting_date >= %(year_start_date)s" \
    #     if report_type == "Profit and Loss" else ""

    if not flt(filters.get("with_period_closing_entry", 0)):
        additional_conditions += " and ifnull(voucher_type, '')!='Period Closing Voucher'"

    gle = frappe.db.sql("""
		SELECT 
    account,
    SUM(debit) AS opening_debit,
    SUM(credit) AS opening_credit
FROM
    `tabGL Entry`
WHERE
    company = %(company)s
    {additional_conditions}
        AND (posting_date < %(from_date)s
        OR IFNULL(is_opening, 'No') = 'Yes')
        AND account IN (SELECT 
            name
        FROM
            `tabAccount`
        WHERE
            report_type = %(report_type)s)
GROUP BY account;""".format(additional_conditions=additional_conditions),
                        {
                            "company": filters.get("company"),
                            "from_date": filters.get("from_date"),
                            "report_type": report_type,
                            "year_start_date": filters.get("year_start_date")
                        },
                        as_dict=True)

    opening = frappe._dict()
    for d in gle:
        opening.setdefault(d.account, d)

    return opening


def calculate_values(accounts, gl_entries_by_account, opening_balances, filters, company_currency):
    init = {
        "opening_debit": 0.0,
        "opening_credit": 0.0,
        "debit": 0.0,
        "credit": 0.0,
        "closing_debit": 0.0,
        "closing_credit": 0.0
    }

    total_row = {
        "account": "Total",
        "account_name": "Total",
        "warn_if_negative": True,
        "opening_debit": 0.0,
        "opening_credit": 0.0,
        "debit": 0.0,
        "credit": 0.0,
        "closing_debit": 0.0,
        "closing_credit": 0.0,
        "parent_account": None,
        "indent": 0,
        "has_value": True,
        "currency": company_currency
    }

    for d in accounts:
        d.update(init.copy())

        # add opening
        d["opening_debit"] = opening_balances.get(d.name, {}).get("opening_debit", 0)
        d["opening_credit"] = opening_balances.get(d.name, {}).get("opening_credit", 0)

        for entry in gl_entries_by_account.get(d.name, []):
            if cstr(entry.is_opening) != "Yes":
                d["debit"] += flt(entry.debit)
                d["credit"] += flt(entry.credit)

        total_row["debit"] += d["debit"]
        total_row["credit"] += d["credit"]
        total_row["opening_debit"] += d["opening_debit"]
        total_row["opening_credit"] += d["opening_credit"]

        total_row["closing_debit"] += (d["debit"] - d["credit"]) if (d["debit"] - d["credit"]) > 0 else 0
        total_row["closing_credit"] += abs(d["debit"] - d["credit"]) if (d["debit"] - d["credit"]) < 0 else 0

    return total_row


def accumulate_values_into_parents(accounts, accounts_by_name):
    for d in reversed(accounts):
        if d.parent_account:
            for key in value_fields:
                accounts_by_name[d.parent_account][key] += d[key]


def prepare_data(accounts, filters, total_row, parent_children_map, company_currency):
    data = []
    total_row["closing_debit"] = 0
    total_row["closing_credit"] = 0
    for d in accounts:
        has_value = False
        row = {
            "account_name": d.account_name,
            "account": d.name,
            "parent_account": d.parent_account,
            "indent": d.indent,
            "from_date": filters.get("from_date"),
            "to_date": filters.get("to_date"),
            "currency": company_currency
        }

        prepare_opening_and_closing(d)

        for key in value_fields:
            row[key] = flt(d.get(key, 0.0), 3)

            if abs(row[key]) >= 0.005:
                # ignore zero values
                has_value = True

        row["has_value"] = has_value
        data.append(row)

        if not d.parent_account:
            total_row["closing_debit"] += (d["debit"] - d["credit"]) if (d["debit"] - d["credit"]) > 0 else 0
            total_row["closing_credit"] += abs(d["debit"] - d["credit"]) if (d["debit"] - d["credit"]) < 0 else 0

    data.extend([{}, total_row])

    return data


def prepare_opening_and_closing(d):
    d["closing_debit"] = d["opening_debit"] + d["debit"]
    d["closing_credit"] = d["opening_credit"] + d["credit"]

    if d["closing_debit"] > d["closing_credit"]:
        d["closing_debit"] -= d["closing_credit"]
        d["closing_credit"] = 0.0

    else:
        d["closing_credit"] -= d["closing_debit"]
        d["closing_debit"] = 0.0

    if d["opening_debit"] > d["opening_credit"]:
        d["opening_debit"] -= d["opening_credit"]
        d["opening_credit"] = 0.0

    else:
        d["opening_credit"] -= d["opening_debit"]
        d["opening_debit"] = 0.0
