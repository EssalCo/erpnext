# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import frappe


def execute():

    item_groups = frappe.db.sql(
        """SELECT `name` FROM 
        `tabItem Group` WHERE (`parent_item_group` IS NULL OR `parent_item_group` = '') ORDER BY `creation` ASC;""", as_dict=True
    )

    for item_group in item_groups:
        ig = frappe.get_doc("Item Group", item_group.name)
        last_existing_serial = frappe.db.sql("""SELECT 
                    MAX(serial * 1) AS maxi
                FROM
                    `tabItem Group`
                WHERE parent_item_group IS NULL;""", as_dict=True)
        if len(last_existing_serial) == 0 or not last_existing_serial[0].maxi:
            # last_existing_serial = 0
            next_serial = 1
        else:
            last_existing_serial = last_existing_serial[0].maxi or 0
            next_serial = last_existing_serial + 1
        frappe.db.sql("""UPDATE `tabItem Group` SET `serial` = '{0}'
                    WHERE `name` = '{1}';""".format(
            next_serial,
            ig.name
        ))
        frappe.db.commit()
        print "PARENT"
        print str(next_serial)
        update_children_serials(ig.name)

    #######################


def update_children_serials(parent_item_group):
    accounts = frappe.db.sql(
        """SELECT `name` FROM 
        `tabItem Group` WHERE  `parent_item_group` = '%(parent)s' ORDER BY `creation` ASC;""",
        dict(parent=parent_item_group), as_dict=True
    )

    if len(accounts) == 0:
        return
    for acc in accounts:
        account = frappe.get_doc("Item Group", acc.name)

        # if not getattr(self, "account_serial_x", None):
        #     send_msg_telegram("return " + str(self.account_serial) + str(self.account_serial_x))
        #     return

        # send_msg_telegram("parent " + str(self.account_serial) + str(self.account_serial_x))

        last_existing_serial = frappe.db.sql("""SELECT serial, name FROM
          `tabItem Group` WHERE
           serial = (
        SELECT 
            MAX(serial * 1) AS maxi
        FROM
            `tabItem Group`
        WHERE 
             parent_item_group = %s
                )
                ORDER BY `creation` ASC LIMIT 1;""", (account.parent_item_group,), as_dict=True)
        parent_serial = frappe.db.get_value(
            "Item Group",
            account.parent_item_group,
            [
                "serial"
            ]
        )
        if len(last_existing_serial) == 0 or not last_existing_serial[0].serial:
            print "Child"
            print parent_serial
            last_existing_serial = int(parent_serial) * 100
            next_serial = last_existing_serial + 1
        else:
            _last_existing_serial = int(last_existing_serial[0].serial)
            next_serial = _last_existing_serial + 1

        # trimmed_serial = str(last_existing_serial[0].account_serial_x).split(".")[-1]
        # next_serial_str = "{0}.{1}".format(parent_serial, int(trimmed_serial) + 1)
        # send_msg_telegram("finish " + str(self.account_serial) + str(self.account_serial_x))
        print str(next_serial)
        frappe.db.sql("""UPDATE `tabItem Group` SET `serial` = '{0}'
                WHERE `name` = '{1}';""".format(
            next_serial,
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
