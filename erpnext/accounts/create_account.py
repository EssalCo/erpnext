# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

import traceback

import frappe
from erpnext.utilities.send_telegram import send_msg_telegram
import urllib


@frappe.whitelist(allow_guest=True)
def create_account():
    # 'account_name',
    # 'is_group' => 'True | False’,
    # 'company',
    # 'root_type' => 'Asset | Liability | Income |Expense |Equity',
    # ‘report_type’ => 'Balance Sheet | Profit and Loss',
    # ‘parent_account’,
    # ‘account_type’ => 'Accumulated Depreciation | Bank | Cash | Chargeable | Cost of Goods Sold | Depreciation | Equity | Expense Account | Expenses Included In Valuation | Fixed Asset | Income Account | Payable | Receivable | Round Off | Stock | Stock Adjustment | Stock Received But Not Billed\nTax | Temporary',
    # ‘tax_rate’,
    # ‘freeze_account’ => 'No | Yes',
    # ‘balance_must_be’ => 'Debit | Credit'
    
    try:
        from frappe.utils import get_site_name
        site_name = get_site_name(frappe.local.request.host)
        data = frappe.form_dict.data
        send_msg_telegram(str(site_name))
        # send_msg_telegram(str(data))
        # if isinstance(data, basestring):
        #     import json
        #     data = json.loads(data)
        send_msg_telegram(str(data))
        # send_msg_telegram(str(site_name))
        # send_msg_telegram(str(frappe.form_dict))
        account_name = data['account_name']
        if account_name and '%' in account_name:
            account_name = urllib.unquote(str(data['account_name'])).decode('utf-8', 'replace')
        # is_group = frappe.form_dict['is_group']
        company = data['company']
        if company and '%' in company:
            company = urllib.unquote(str(data['company'])).decode('utf-8', 'replace')
        root_type = data.get('root_type', 'Expense')
        report_type = data.get('report_type')
        parent_account = data.get('parent_account')
        if parent_account and '%' in parent_account:
            parent_account = urllib.unquote(str(data.get('parent_account'))).decode('utf-8', 'replace')
        account_type = data.get('account_type')
        if account_type and '%' in account_type:
            account_type = urllib.unquote(str(data.get('account_type'))).decode('utf-8', 'replace')
        tax_rate = data.get('tax_rate')
        freeze_account = data.get('freeze_account')
        balance_must_be = data.get('balance_must_be')
        prev_account = frappe.db.sql(
            """SELECT `name` FROM `tabAccount` WHERE (
            `name` LIKE '%- {0} - {2}' 
            OR `name` LIKE '% - {2} - {0}' 
            OR `name` LIKE '{2} - {0}'
            OR `name` LIKE '{0} - {2}'
            ) AND `company` = '{1}';""".format(
                account_name,
                company,
                frappe.get_value(
                    "Company",
                    company,
                    "abbr"
                )
            ), as_dict=True
        )

        if len(prev_account) != 0:
            return dict(status=True, message="Account is added to erpnext successfully", account=prev_account[0].name)

        if not parent_account and not (
            root_type and report_type and account_type and tax_rate and freeze_account and balance_must_be):
            frappe.throw("You must send all data since this is a parent account")
        if parent_account:
            # send_msg_telegram(str(parent_account))
            parent_account_data = frappe.get_value("Account", parent_account, 
                            [
                                "root_type", 
                                "report_type", 
                                "account_type", 
                                "tax_rate",
                                "freeze_account",
                                "balance_must_be",
                                "is_group"
                            ], as_dict=True)

            if not parent_account_data:
                frappe.throw("The parent account you chose does not existing.")
            if not root_type:
                root_type = parent_account_data.root_type
            if not report_type:
                report_type = parent_account_data.report_type
            if not account_type:
                account_type = parent_account_data.account_type
            if not tax_rate:
                tax_rate = parent_account_data.tax_rate
            if not freeze_account:
                freeze_account = parent_account_data.freeze_account
            if not balance_must_be:
                balance_must_be = parent_account_data.balance_must_be
            if not parent_account_data.is_group:
                frappe.db.set_value("Account", parent_account, "is_group", 1)

        account = frappe.get_doc(
            dict(
                doctype="Account",
                account_name=account_name,
                is_group=0 if parent_account else 1,
                company=company,
                root_type=root_type,
                report_type=report_type,
                parent_account=parent_account,
                account_type=account_type,
                tax_rate=tax_rate,
                freeze_account=freeze_account,
                balance_must_be=balance_must_be
            )
        )
        account.flags.ignore_mandatory = True
        account.insert(ignore_permissions=True)
        frappe.db.commit()

        return dict(status=True, message="Account is added to erpnext successfully", account=account.name)
    except Exception as e:

        error_msg = traceback.format_exc()
        send_msg_telegram(error_msg)



