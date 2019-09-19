from datetime import datetime

from umalqurra.hijri_date import HijriDate

import frappe


@frappe.whitelist(allow_guest=True)
def convert_to_hijri(date):
    if not date:
        return ""
    if len(str(date))>10:
        date = str(date).split(" ")[0]
    day = int(datetime.strptime(str(date), '%Y-%m-%d').strftime('%d'))
    month = int(datetime.strptime(str(date), '%Y-%m-%d').strftime('%m'))
    year = int(datetime.strptime(str(date), '%Y-%m-%d').strftime('%Y'))

    hijri_date = HijriDate(year, month, day, gr=True)
    hijri_date = "{0}-{1}-{2} \n {3}".format(int(hijri_date.day),
                                      int(hijri_date.month),
                                      int(hijri_date.year),
                                      hijri_date.month_name,
                                      )
    return hijri_date
