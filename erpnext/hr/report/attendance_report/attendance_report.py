# Copyright (c) 2013, nana.sa and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
from __future__ import unicode_literals
from __future__ import unicode_literals

import frappe


def execute(filters=None):
    columns = get_columns()
    data = get_report_data(filters)
    return columns, data


def get_columns():
    return [

        "{label}:{type}:{width}".format(label="Employee ID", type="Link/Employee", width=100),
        "{label}:{type}:{width}".format(label="Employee Name", type="Data", width=150),
        "{label}:{type}:{width}".format(label="Department", type="Data", width=150),
        "{label}:{type}:{width}".format(label="Date", type="Date", width=120),
        "{label}:{type}:{width}".format(label="On duty", type="Data", width=100),
        "{label}:{type}:{width}".format(label="Off duty", type="Data", width=100),
        "{label}:{type}:{width}".format(label="Clock In", type="Data", width=100),
        "{label}:{type}:{width}".format(label="Clock Out", type="Data", width=100),
        "{label}:{type}:{width}".format(label="Late", type="Data", width=70),
        "{label}:{type}:{width}".format(label="Early", type="Data", width=70),
        "{label}:{type}:{width}".format(label="Work Time", type="Data", width=100),
        "{label}:{type}:{width}".format(label="Status", type="Data", width=150),
        "{label}:{type}:{width}".format(label="OT Time", type="Data", width=100),
        "{label}:{type}:{width}".format(label="ATT Time", type="Data", width=100),
        "{label}:{type}:{width}".format(label="NDays", type="Int", width=100),
        "{label}:{type}:{width}".format(label="NDays_OT", type="Float", width=100),
        "{label}:{type}:{width}".format(label="Must C/IN", type="Check", width=100),
        "{label}:{type}:{width}".format(label="Must C/Out", type="Check", width=100),
        "{label}:{type}:{width}".format(label="Normal", type="Check", width=100),
        "{label}:{type}:{width}".format(label="Real time", type="Check", width=100)

    ]


def get_report_data(filters):
    attendance_filters = {}

    if filters.get('status', None):
        attendance_filters.update({'status': filters.get('status')})

    if filters and "employee" in filters:
        attendance_filters.update({'employee': filters.get('employee')})

    if filters and "from_date" in filters and "to_date" in filters:
        attendance_filters.update({"attendance_date": ("between", [filters["from_date"], filters["to_date"]])})

    attendance_list = frappe.get_list("Attendance",
                                      fields=["*"],
                                      filters=attendance_filters,
                                      ignore_permissions=True
                                      )

    report_rows = []
    from datetime import datetime
    for attendance in attendance_list:
        on_duty = datetime.strptime(attendance.on_duty,"%H:%M").strftime("%H:%M") if attendance.on_duty else None
        off_duty = datetime.strptime(attendance.off_duty,"%H:%M").strftime("%H:%M") if attendance.off_duty else None
        clock_in = datetime.strptime(attendance.clock_in,"%H:%M").strftime("%H:%M") if attendance.clock_in else None
        clock_out = datetime.strptime(attendance.clock_out,"%H:%M").strftime("%H:%M") if attendance.clock_out else None
        work_time = datetime.strptime(attendance.work_time,"%H:%M").strftime("%H:%M") if attendance.work_time else None
        ot_time = datetime.strptime(attendance.ot_time,"%H:%M").strftime("%H:%M") if attendance.ot_time else None
        att_time = datetime.strptime(attendance.att_time,"%H:%M").strftime("%H:%M") if attendance.att_time else None
        late,early = "00:00","00:00"
        if clock_in and on_duty and clock_in>on_duty:
            late = datetime.strptime(attendance.clock_in,"%H:%M") - datetime.strptime(attendance.on_duty,"%H:%M")

        if clock_out and off_duty and off_duty>clock_out:
            early = datetime.strptime(attendance.off_duty, "%H:%M") - datetime.strptime(attendance.clock_out, "%H:%M")

        report_rows.append(
            [
                attendance.employee,
                attendance.employee_name,
                attendance.department,
                attendance.attendance_date,
                on_duty,
                off_duty,
                clock_in,
                clock_out,
                late,
                early,
                work_time,
                attendance.status,
                ot_time,
                att_time,
                attendance.ndays,
                attendance.ndays_ot,
                attendance.c_in,
                attendance.c_out,
                attendance.normal,
                attendance.real_time
                # agent.creation.strftime('%Y-%m-%d') if agent.creation else "",

            ]
        )

    return report_rows
