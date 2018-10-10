# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt
from __future__ import unicode_literals

import math

import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import date_diff, flt, getdate, nowdate


class EndofServiceAward(Document):
    def validate(self):
        sal = self.get_salary(self.employee)
        if sal:
            self.salary = sal
            # if hasattr(self,"workflow_state"):
            #     if "Rejected" in self.workflow_state:
            #         self.docstatus = 1
            #         self.docstatus = 2
            # self.switch_workflow_transition()
            # frappe.throw(str(self.months))

    def on_submit(self):

        self.validate_expense_claim_type()

        expenses = []
        if self.award > 0:
            expenses.append(
                {
                    "doctype": "Expense Claim Detail",
                    "parenttype": "Expense Claim",
                    "parentfield": "expenses",
                    "expense_date": nowdate(),
                    "expense_type": 'End of Service',
                    "claim_amount": round(self.award),
                    "sanctioned_amount": round(self.award)
                }
            )
        if self.leave_total_cost > 0:
            expenses.append(
                {
                    "doctype": "Expense Claim Detail",
                    "parenttype": "Expense Claim",
                    "parentfield": "expenses",
                    "expense_date": nowdate(),
                    "expense_type": 'Leave',
                    "claim_amount": round(self.leave_total_cost),
                    "sanctioned_amount": round(self.leave_total_cost)
                }
            )
        if len(expenses) > 0:
            ec_doc = frappe.get_doc({
                "doctype": "Expense Claim",
                "exp_approver": 'Administrator',
                "posting_date": nowdate(),
                "employee": self.employee,
                "expenses": expenses,
                "employee_name": self.employee_name,
                "company": frappe.defaults.get_user_default("Company")
            }).insert(ignore_permissions=True)
            msg = """Expense cliam has been created: <b><a href="#Form/Expense Claim/{0}">{0}</a></b>""".format(
                ec_doc.name)
            frappe.msgprint(_(msg))

    def validate_expense_claim_type(self):
        leave = frappe.get_value("Expense Claim Type", "Leave")
        if not leave:
            frappe.throw(_("Please Create <b>Leave</b> Expense Claim Type"))
        eos = frappe.get_value("Expense Claim Type", "End of Service")
        if not eos:
            frappe.throw(_("Please Create <b>End of Service</b> Expense Claim Type"))

    def get_salary(self, employee):

        result = frappe.db.sql(
            "select net_pay from `tabSalary Slip` where employee='{0}' order by creation desc limit 1".format(employee))
        if result:
            return result[0][0]
        else:
            frappe.throw(_("No salary slip found for this employee"))

    def get_leave_balance(self, employee):
        employee_details = frappe.get_value(
            "Employee",
            employee,
            [
                "date_of_joining",
                "contract_end_date"
            ], as_dict=True
        )
        from datetime import datetime
        if (datetime.strptime(str(employee_details.contract_end_date), '%Y-%m-%d').date() - datetime.strptime(
                str(employee_details.date_of_joining), '%Y-%m-%d').date()).days < 365:
            return 0
        total_leave_balance = frappe.db.sql(
            """select 
    total_leaves_allocated,
    from_date,
    to_date,
    name 
from 
    `tabLeave Allocation` 
where 
    employee='{0}' 
order by creation desc 
limit 1;""".format(
                employee))
        if total_leave_balance:
            leave_days = frappe.db.sql(
                """select 
    COALESCE(sum(total_leave_days), 0) 
from 
    `tabLeave Application` 
where 
    employee='{0}' 
        and docstatus =1 
        and posting_date between '{1}' and '{2}';""".format(
                    employee, total_leave_balance[0][1], total_leave_balance[0][2]))[0][0]
            if not leave_days:
                leave_days = 0
            leave_balance = int(total_leave_balance[0][0]) - int(leave_days)
            return leave_balance

    def switch_workflow_transition(self):
        employee_user = frappe.get_value("Employee", filters={"name": self.employee}, fieldname="user_id")
        if hasattr(self, "workflow_state") and employee_user:
            if self.workflow_state == "Approved By IT Support":
                if u'Director' in frappe.get_roles(employee_user):
                    self.workflow_state = "Approved By IT Support (CEO)"
                elif u'Manager' in frappe.get_roles(employee_user):
                    self.workflow_state = "Approved By IT Support (Dir.)"

    def unallowed_actions(self):
        if hasattr(self, "workflow_state"):
            permitted_departments = frappe.db.sql_list(
                "select for_value from `tabUser Permission` where allow = 'Department' and user = '{0}'".format(
                    frappe.session.user))
            if self.department not in permitted_departments and 'Manager' in frappe.get_roles(
                    frappe.session.user) and self.workflow_state == "Approved By IT Support":
                return True
            elif self.department not in permitted_departments and 'Director' in frappe.get_roles(
                    frappe.session.user) and self.workflow_state == "Approved By IT Support (Dir.)":
                return True
            elif self.workflow_state in ["Approved by Manager", "Approved By Director", "Approved By CEO"]:
                employee_user = frappe.get_value("Employee", filters={"name": self.employee}, fieldname="user_id")
                if employee_user != frappe.session.user:
                    return True

                    # def get_salary(self,employee):
                    #     start_date = get_first_day(getdate(nowdate()))
                    #     end_date = get_last_day(getdate(nowdate()))
                    #     doc = frappe.new_doc("Salary Slip")
                    #     doc.salary_slip_based_on_timesheet="0"

                    #     doc.payroll_frequency= "Monthly"
                    #     doc.start_date= start_date
                    #     doc.end_date= end_date
                    #     doc.employee= self.employee
                    #     doc.employee_name= self.employee_name
                    #     doc.company= "Tawari"
                    #     doc.posting_date= start_date

                    #     doc.insert(ignore_permissions = True)


                    #     grosspay =doc.gross_pay
                    #     result=grosspay
                    #     if result:
                    #         return result
                    #     else:
                    #         frappe.throw("لا يوجد قسيمة راتب لهذا الموظف")


@frappe.whitelist()
def get_award(start_date, end_date, salary, toc, reason):
    # doc = json.loads(EOS_doc)
    start = start_date
    end = end_date
    ret_dict = {}

    if getdate(end) < getdate(start):
        frappe.throw(_("Work start date should be before end date"));
    else:
        diffDays = date_diff(end, start)
        years = math.floor(diffDays / 365)
        daysrem = diffDays - (years * 365)
        months = math.floor(daysrem / 30.416)
        days = math.ceil(daysrem - (months * 30.416))
        ret_dict = {"days": days, "months": months, "years": years}
    # salary = doc['salary']
    years = flt(years) + (flt(months) / 12) + (flt(days) / 365)
    # reason = doc['reason']
    if not reason:
        frappe.throw(_("Please select the reason end of service "))
    else:
        if toc == "Limited":
            if reason == "فسخ العقد من قبل صاحب العمل لأحد الحالات الواردة في المادة (80)" or reason == "فسخ العقد من قبل الموظف أو ترك الموظف العمل لغير الحالات الواردة في المادة (81)":
                ret_dict["award"] = 0
            else:
                firstPeriod, secondPeriod = 0, 0
                if years > 5:
                    firstPeriod = 5
                    secondPeriod = years - 5
                else:
                    firstPeriod = years
                result = (firstPeriod * salary * 0.5) + (secondPeriod * salary)
                ret_dict["award"] = result
        else:
            # elif toc == "دوام كامل"

            if reason == "فسخ العقد من قبل صاحب العمل لأحد الحالات الواردة في المادة (80)" or reason == "ترك الموظف العمل دون تقديم استقالة لغير الحالات الواردة في المادة (81)":
                ret_dict["award"] = 0
            elif reason == "استقالة الموظف":
                if years < 2:
                    result = 0
                elif years <= 5:
                    result = (1.0 / 6.0) * salary * years
                elif years <= 10:
                    result = ((1.0 / 3.0) * salary * 5) + ((2.0 / 3.0) * salary * (years - 5))
                else:
                    result = (0.5 * salary * 5) + (salary * (years - 5))
                ret_dict["award"] = result
            else:
                if years <= 5:
                    result = 0.5 * salary * years
                else:
                    result = (0.5 * salary * 5) + salary * (years - 5)
                ret_dict["award"] = result

    return ret_dict


def get_permission_query_conditions(user):
    pass
    # if not user: user = frappe.session.user
    # employees = frappe.get_list("Employee", fields=["name"], filters={'user_id': user}, ignore_permissions=True)
    # if employees:
    #     query = ""
    #     employee = frappe.get_doc('Employee', {'name': employees[0].name})

    #     if u'Employee' in frappe.get_roles(user):
    #         if query != "":
    #             query+=" or "
    #         query+=""" employee = '{0}'""".format(employee.name)
    #     return query
