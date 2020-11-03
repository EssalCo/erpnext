# -*- coding: utf-8 -*-


import  frappe


def execute():
    company = "أعمال النماء"
    entries = frappe.db.sql("""SELECT name, cost_center, project from `tabGL Entry` where voucher_type='Journal Entry' and company = '{0}'
     and project is null and cost_center is not null;""".format(
        company
    ), as_dict=True)

    for entry in entries:
        print entry.name
        # print str(entry.cost_center)

        cost_center = frappe.get_value(
            "Cost Center",
            dict(
                name=entry.cost_center
            ), "cost_center_name"
        )
        # print cost_center
        if cost_center:
            project = frappe.get_value(
                "Project",
                dict(
                    project_name=cost_center,
                    # company=company
                ), "name"
            )
            if project:
                print("project found")
                frappe.db.sql(
                    """update `tabGL Entry` SET project = '{0}' WHERE name = '{1}';""".format(
                        project,
                        entry.name
                    )
                )
                pass
            else:
                print("ERROR: no project found!!")
                continue
        else:
            print("ERROR: no cost center!!")
            continue

    entries = frappe.db.sql("""SELECT a.name, a.cost_center from `tabJournal Entry Account` a 
     INNER JOIN `tabJournal Entry` j ON j.name = a.parent and j.company = '{0}' 
    WHERE a.project is null and a.cost_center is not null;""".format(
        company
    ), as_dict=True)
    for entry in entries:
        print entry.name
        # print str(entry.cost_center)

        cost_center = frappe.get_value(
            "Cost Center",
            dict(
                name=entry.cost_center
            ), "cost_center_name"
        )
        # print cost_center
        if cost_center:
            project = frappe.get_value(
                "Project",
                dict(
                    project_name=cost_center,
                    # company=company
                ), "name"
            )
            # print str(project)
            if project:
                print("project found")

                frappe.db.sql(
                    """update `tabJournal Entry Account` SET project = '{0}' WHERE name = '{1}';""".format(
                        project,
                        entry.name
                    )
                )
            else:
                print("ERROR: no project found!!")
                continue
        else:
            print("ERROR: no cost center!!")
            continue