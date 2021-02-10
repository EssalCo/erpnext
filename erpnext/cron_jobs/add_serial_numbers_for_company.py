# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import frappe


def execute():

    # update tabAccount set account_name = REPLACE(account_name, CONCAT(LEFT(account_name,LOCATE(' -',account_name) - 1), " - "), "")
    # where `company` ="AL Mather Trading EST";

    #
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:31.781014" where name = "الأصــــول - م";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:33.041162" where name = "الخصــــــوم - م";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:34.739865" where name = "حقوق الملكية - م";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:35.677015" where name = "الإيرادات - م";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:35.886136" where name = "المصــــــــــروفات - م";""")


    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:31.781014" where name = "الأصــــول - أ";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:33.041162" where name = "الخصــــــوم - أ";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:34.739865" where name = "حقوق الملكية - أ";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:35.677015" where name = "الإيرادات - أ";""")
    frappe.db.sql(
        """update tabAccount set creation = "2018-07-22 16:04:35.886136" where name = "المصــــــــــروفات - أ";""")


    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:55.995594" where name = "Assets - Z";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.187852" where name = "Liabilities - Z";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.341230" where name = "Owners Equity - Z";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.782180" where name = "Income - Z";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:57.665961" where name = "Expenses - Z";""")


    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:55.995594" where name = "Assets - D";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.187852" where name = "Liabilities - D";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.341230" where name = "Owners Equity - D";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.782180" where name = "Revenue - D";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:57.665961" where name = "Expenses - D";""")


    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:55.995594" where name = "Assets - I";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.187852" where name = "Source of Funds (Liabilities) - I";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.341230" where name = "Equity - I";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.782180" where name = "Revenue - I";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:57.665961" where name = "Expenses - I";""")


    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:55.995594" where name = "الأصــــول - M";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.187852" where name = "الخصــــــوم  - M";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.341230" where name = "حقوق الملكية - M";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.782180" where name = "الإيرادات - M";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:57.665961" where name = "المصروفات - M";""")

    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:55.995594" where name = "الأصــــول - ARH";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.187852" where name = "الخصــــــوم - ARH";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.341230" where name = "حقوق الملكية - ARH";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:56.782180" where name = "الإيرادات - ARH";""")
    frappe.db.sql(
        """update tabAccount set creation = "2019-03-26 09:42:57.665961" where name = "المصــــــــــروفات - ARH";""")

    companies = frappe.get_list(
        "Company",
        fields=["name"],
        filters=dict(
            name=("in", [
                "Abdulaziz Almashal Farm",
                "Awqaf Almashal",
                "شركة مناف للإستثمار والتطوير العقاري",
                "Murbiha Holding company",
                "Investments CDR",
                "DR ABDULAZIZ HAMAD ALMASHAL",
                "DR ABDULAZIZ",
            ])
        ),
        ignore_permissions=True
    )

    for _company in companies:
        company = _company.name
        frappe.db.sql(
            """UPDATE
                        `tabAccount` SET `account_serial` = '', account_serial_x = ''
                        WHERE `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )
        accounts = frappe.db.sql(
            """SELECT `name`, `company` FROM 
            `tabAccount` WHERE (`parent_account` IS NULL OR `parent_account` = '') 
            AND `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )

        for acc in accounts:
            account = frappe.get_doc("Account", acc.name)
            last_existing_serial = frappe.db.sql("""SELECT 
        MAX(account_serial) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account IS NULL;""", (company,), as_dict=True)
            if len(last_existing_serial) == 0 or not last_existing_serial[0].maxi:
                # last_existing_serial = 0
                next_serial = 1
                next_serial_str = "#1"
            else:
                last_existing_serial = last_existing_serial[0].maxi
                next_serial = int(last_existing_serial or 0) + 1
                next_serial_str = "#{0}".format(next_serial)
            frappe.db.sql("""UPDATE `tabAccount` SET `account_serial` = '{0}',
                         `account_serial_x` = '{1}' WHERE `name` = '{2}';""".format(
                int(next_serial),
                next_serial_str,
                account.name
            ))
            frappe.db.commit()
            print "PARENT"
            print str(next_serial)
            print str(next_serial_str)
            update_children_serials(account.name)

        #######################
        accounts = frappe.db.sql(
            """SELECT `name`, `company`, `account_name`, `account_serial` FROM 
            `tabAccount` WHERE `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )

        for account in accounts:
            # serial = account.account_name.split(" -")[0]
            # if serial.isdigit():
            #     account.account_name = account.account_name.replace(account.account_name.split(" -")[0], "")[2:]
            frappe.db.set_value(
                "Account",
                account.name,
                "account_name",
                "{0} - {1}".format(account.account_serial, account.account_name)
            )


def update_children_serials(parent_account):
    accounts = frappe.db.sql(
        """SELECT `name` FROM 
        `tabAccount` WHERE  `parent_account` = %(parent)s ORDER BY `creation` ASC;""",
        dict(parent=parent_account), as_dict=True
    )

    if len(accounts) == 0:
        return
    for acc in accounts:
        account = frappe.get_doc("Account", acc.name)
        print("CHILD")
        # if not getattr(self, "account_serial_x", None):
        #     send_msg_telegram("return " + str(self.account_serial) + str(self.account_serial_x))
        #     return

        # send_msg_telegram("parent " + str(self.account_serial) + str(self.account_serial_x))

        last_existing_serial = frappe.db.sql("""SELECT account_serial, account_serial_x, name FROM
      `tabAccount` WHERE
       account_serial = (
    SELECT 
        MAX(account_serial * 1) AS maxi
    FROM
        tabAccount
    WHERE 
        company = %s
            AND parent_account = %s);""", (account.company, account.parent_account), as_dict=True)
        parent_serial, account_serial_x = frappe.db.get_value(
            "Account",
            account.parent_account,
            [
                "account_serial",
                "account_serial_x"
            ]
        )
        # send_msg_telegram("parent acc " + str(parent_serial) + " " + str(account_serial_x))
        # send_msg_telegram("parent account " + str(last_existing_serial))

        if len(last_existing_serial) == 0 or not int(last_existing_serial[0].account_serial or 0):
            print("NOT FOUND")
            print(parent_serial)
            last_existing_serial = long(parent_serial) * 100
            print(last_existing_serial + 1)

            # send_msg_telegram("sum " + str(last_existing_serial))
            next_serial = last_existing_serial + 1
            next_serial_str = "{0}.{1}".format(parent_serial, 1)
        else:
            print("FOUND")
            print(last_existing_serial[0].account_serial)
            last_existing_serial = long(last_existing_serial[0].account_serial)
            # send_msg_telegram("query " + str(last_existing_serial))

            next_serial = last_existing_serial + 1

            # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
            next_serial_str = "{0}.{1}".format(account_serial_x, next_serial)

            # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
            # next_serial_str = "{0}.{1}".format(parent_serial, int(trimmed_serial) + 1)
        # send_msg_telegram("finish " + str(self.account_serial) + str(self.account_serial_x))
        print(str(next_serial_str))
        print(str(next_serial))
        frappe.db.sql("""UPDATE `tabAccount` SET `account_serial` = '{0}', 
        `account_serial_x` = '{1}' WHERE `name` = '{2}';""".format(
            int(next_serial),
            next_serial_str,
            account.name
        ))
        frappe.db.commit()

        update_children_serials(account.name)
    # self.account_serial = int(next_serial_str.replace(".", "").replace("#", ""))
    # self.account_serial_x = next_serial_str
    # except Exception as e:
    #     print str(e)
    # account.get_account_serial()
    # account.save(ignore_permissions=True)


def execute_again():
    companies = frappe.get_list(
        "Company",
        fields=["name", "abbr"],
        filters=dict(
            name=("in", [
                "Abdulaziz Almashal Farm",
                "Awqaf Almashal",
                "شركة مناف للإستثمار والتطوير العقاري",
                "Murbiha Holding company",
                "Investments CDR",
                "DR ABDULAZIZ HAMAD ALMASHAL",
                "DR ABDULAZIZ",
            ])
        ),
        ignore_permissions=True
    )
    to_be_replaced = frappe.db.sql(
        """select fieldname, parent from tabDocField where fieldtype = "Link" and `options` = "Account";""",
        as_dict=True
    )
    for _company in companies:
        company = _company.name

        accounts = frappe.db.sql(
            """SELECT `name`, `account_name` FROM 
            `tabAccount` WHERE `company` = '{0}' ORDER BY `creation` ASC;""".format(
                company
            ), as_dict=True
        )
        try:
            print(company)
        except: pass
        for account in accounts:
            old_name = account.name
            new_name = account.account_name
            try:
                frappe.db.sql("UPDATE tabAccount SET name = '{0}' WHERE name = '{1}';".format(
                    new_name,
                    old_name
                ))
            except:
                old_name = account.name
                new_name = account.account_name.strip() + " - " + _company.abbr
                frappe.db.sql("UPDATE tabAccount SET name = '{0}' WHERE name = '{1}';".format(
                    new_name,
                    old_name
                ))

            frappe.db.sql("UPDATE tabAccount SET parent = '{0}' WHERE parent = '{1}';".format(
                new_name,
                old_name
            ))
            frappe.db.sql("UPDATE tabAccount SET parent_account = '{0}' WHERE parent_account = '{1}';".format(
                new_name,
                old_name
            ))
            for field in to_be_replaced:
                print(field)
                try:
                    frappe.db.sql(
                        "UPDATE `tab{doctype}` SET `{field}` = '{new_name}' WHERE `{field}` = '{old_name}';".format(
                            doctype=field.parent,
                            field=field.fieldname,
                            new_name=new_name,
                            old_name=old_name
                        ))
                except Exception as e:
                    print(e)
