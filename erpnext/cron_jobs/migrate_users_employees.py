# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path
from umalqurra.hijri_date import HijriDate
from datetime import datetime


def execute():
    users = "/private/files/tahlia_emplyee.csv"

    print("Starting users..")
    company = frappe.get_doc(
        "Company",
        dict(
            company_name="Tahlia"
        )
    )
    current_file = get_file_path(users)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        departments = list(set([row[5] for row in spamreader if row[5]]))

        for department in departments:
            frappe.get_doc(dict(
                doctype="Department",
                department_name=department)).insert(ignore_permissions=True)

        for row in spamreader:
            try:
                id_no = int(row[0])
            except:
                continue
            birth_date = row[1]
            if birth_date:
                if " م" in birth_date:
                    birth_date = str(datetime.strptime(
                        str(birth_date.replace(" م", "")), '%d/%m/%Y'
                    ))
                else:
                    birth_date = str(birth_date.decode('utf-8')).split("/")
                    day = int(birth_date[0].replace(" ", ""))
                    month = int(birth_date[1].replace(" ", ""))
                    year = int(birth_date[2].replace(" ", ""))
                    birth_date = HijriDate(year, month, day, gr=False)
                    birth_date = "{:04d}-{:02d}-{:02d}".format(int(birth_date.year_gr), int(birth_date.month_gr),
                                                           int(birth_date.day_gr))

            full_name = row[2]
            nationality = row[3]
            position = row[4]
            department = row[5]
            date_of_joining = row[6]
            if date_of_joining:
                if " م" in date_of_joining:
                    date_of_joining = str(datetime.strptime(
                        str(date_of_joining.replace(" م", "")), '%d/%m/%Y'
                    ))
            else:
                date_of_joining = str(date_of_joining.decode('utf-8')).split("/")
                day = int(date_of_joining[0].replace(" ", ""))
                month = int(date_of_joining[1].replace(" ", ""))
                year = int(date_of_joining[2].replace(" ", ""))
                date_of_joining = HijriDate(year, month, day, gr=False)
                date_of_joining = "{:04d}-{:02d}-{:02d}".format(int(date_of_joining.year_gr), int(date_of_joining.month_gr),
                                                           int(date_of_joining.day_gr))
            position_for = row[13]

            residence_valid_to = row[15]
            if residence_valid_to:
                if " م" in residence_valid_to:
                    residence_valid_to = str(datetime.strptime(
                        str(residence_valid_to.replace(" م", "")), '%d/%m/%Y'
                    ))
            address = location = row[16]
            mobile = row[18]
            email = row[17] or "{0}@tahlia.s1.essal.co".format(id_no)
            names = full_name.split[" "]
            user = frappe.get_doc(dict(
                doctype="User",
                enabled=1,
                email=email,
                first_name=names[0],
                middle_name=names[1] if len(names) > 1 else None,
                last_name=names[len(names) - 1],
                full_name=full_name,
                send_welcome_email=0,
                unsubscribed=0,
                username=id_no,
                language="ar",
                roles=[

                ],
                gender="Female" if "ة" in full_name else "Male",
                phone="00966{0}".format(mobile),
                mobile_no=mobile,
                birth_date=birth_date,
                location=address,
                bio="{4} - {0} - {1} - {2} - {3}".format(nationality, position, location, position_for, id_no),
                user_type="System User",

            )
            )
            user.insert(ignore_permissions=True)

            employee = frappe.get_doc(
                dict(
                    doctype='Employee',
                    employee_name=full_name,
                    naming_series="EMP/",
                    company=company.name,
                    user_id=user.name,
                    employee_number=id_no,
                    date_of_joining=date_of_joining,
                    date_of_birth=birth_date,
                    gender=user.gender,
                    status="Active",
                    department=department,
                    cell_number=user.phone,
                    personal_email=user.email,
                    permanent_address=address,
                    current_address=address,
                    bio=user.bio,
                    place_of_issue=nationality,
                    residence_valid_to=residence_valid_to,
                )

            )
            employee.insert(ignore_permissions=True)
            user.append_roles("Employee", )
            user.save(ignore_permissions=True)
            frappe.db.commit()