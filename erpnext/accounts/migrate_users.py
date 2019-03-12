import frappe
import requests
import json


def execute():
    url = 'https://serafico.s1.essal.co/api/method/erpnext.accounts.get_companies.get_users'
    response = requests.request("POST", url)
    print response
    result = json.loads(response.text)
    users = result['message']['users']

    print len(users)
    for user in users:

        new_order_dict = dict()
        for key in user:
            new_order_dict[key] = user[key]

        new_order_dict["doctype"] = "User"

        new_doc = frappe.get_doc(new_order_dict)
        new_doc.insert(ignore_permissions=1)

        frappe.db.sql("""UPDATE `tabUser` SET `name` = %s WHERE `name` = %s""", (user.name, new_doc.name))
        print new_doc.name, user['name']

    employees = result['message']['employees']

    print len(employees)
    for employee in employees:

        new_order_dict = dict()
        for key in employee:
            new_order_dict[key] = employee[key]

        new_order_dict["doctype"] = "Employee"

        new_doc = frappe.get_doc(new_order_dict)
        new_doc.insert(ignore_permissions=1)

        print new_doc.name, employee['name']
        
        
# import frappe
# import requests
# import json
# 
# 
# def execute():
#     url = 'https://serafico.s1.essal.co/api/method/erpnext.accounts.get_companies.get_users'
#     response = requests.request("POST", url)
#     print response
#     result = json.loads(response.text)
#     types = result['message']['users']
# 
#     print len(types)
#     for user in types:
# 
#         new_order_dict = dict()
#         for key in user:
#             new_order_dict[key] = user[key]
# 
#         new_doc = frappe.get_doc(new_order_dict)
#         new_doc.insert(ignore_permissions=1)
#     frappe.db.commit()
#     employees = result['message']['employees']
# 
#     print len(employees)
#     for employee in employees:
# 
#         new_order_dict = dict()
#         for key in employee:
#             new_order_dict[key] = employee[key]
# 
#         new_order_dict["doctype"] = "Employee"
# 
#         new_doc = frappe.get_doc(new_order_dict)
#         new_doc.insert(ignore_permissions=1)
# 
#         frappe.db.sql("""UPDATE `tabEmployeer` SET `name` = %s WHERE `name` = %s""", (employee['name'], new_doc.name))
#         print new_doc.name, employee['name']

