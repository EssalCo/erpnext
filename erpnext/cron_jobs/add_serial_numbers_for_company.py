# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import math
from datetime import datetime, timedelta

import frappe


def execute():
    company = "شركة ابعاد فنية للمقاولات"
    accounts = frappe.db.sql(
        """SELECT `name` FROM 
        `tabAccount` WHERE `company` = %(company)s ORDER BY `creation` DESC;""", dict(company=company), as_dict=True
    )

    for acc in accounts:
        account = frappe.get_doc("Account", acc.name)
        try:
            # if not getattr(self, "account_serial_x", None):
            #     send_msg_telegram("return " + str(self.account_serial) + str(self.account_serial_x))
            #     return
            if not account.parent_account:
                # send_msg_telegram("no parent " + str(self.account_serial) + str(self.account_serial_x))

                last_existing_serial = frappe.db.sql("""SELECT 
            MAX(account_serial) AS maxi
        FROM
            tabAccount
        WHERE 
            company = %s
                AND parent_account IS NULL;""", (account.company,), as_dict=True)
                if len(last_existing_serial) == 0:
                    # last_existing_serial = 0
                    # next_serial = 1
                    next_serial_str = "#1"
                else:
                    last_existing_serial = last_existing_serial[0].maxi
                    # next_serial = last_existing_serial + 1
                    next_serial_str = "#{0}".format(last_existing_serial + 1)
            else:
                # send_msg_telegram("parent " + str(self.account_serial) + str(self.account_serial_x))

                last_existing_serial = frappe.db.sql("""SELECT account_serial, account_serial_x, name FROM
          `tabAccount` WHERE
           account_serial = (
        SELECT 
            MAX(account_serial) AS maxi
        FROM
            tabAccount
        WHERE 
            company = %s
                AND parent_account = %s);""", (account.company, account.parent_account), as_dict=True)
                parent_serial = frappe.db.get_value(
                    "Account",
                    account.parent_account,
                    "account_serial"
                )
                if len(last_existing_serial) == 0:
                    # last_existing_serial = parent_serial * 10
                    # next_serial = last_existing_serial + 1
                    next_serial_str = "{0}.{1}".format(parent_serial, 1)
                else:
                    trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
                    next_serial_str = "{0}.{1}".format(parent_serial, int(trimmed_serial) + 1)
            # send_msg_telegram("finish " + str(self.account_serial) + str(self.account_serial_x))

            frappe.db.sql("""UPDATE `tabAccount` SET `account_serial` = '{0}'
            AND `account_serial_x` = '{1}'""".format(
                int(next_serial_str.replace(".", "").replace("#", "")),
                next_serial_str
            ))
            # self.account_serial = int(next_serial_str.replace(".", "").replace("#", ""))
            # self.account_serial_x = next_serial_str
        except Exception as e:
            print str(e)
        # account.get_account_serial()
        # account.save(ignore_permissions=True)