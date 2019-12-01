# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import sys

import frappe

sys.path.append('../..')
import csv
from frappe.utils.file_manager import get_file_path
from datetime import datetime
reload(sys)
sys.setdefaultencoding('utf8')


def execute_again():
    payment_details = "/private/files/nadi_journals_2.csv"

    from_account = "20203 - ايرادات سندات القبض - N"
    to_account = "3030601 - نقد - N"
    print("Starting payments..")

    company = frappe.get_doc(
        "Company",
        dict(
            company_name="Nahdi"
        )
    )
    main_cost_center = "رئيسي - N"

    current_file = get_file_path(payment_details)

    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            # print row
            try:
                serial_no = int(row[0])
            except:
                continue
            amount = float(row[1])
            pay_date = row[2]
            post_date = datetime.strptime(
                str(pay_date), '%Y/%m/%d'
            )
            pay_name = str(row[3])
            akarno = row[4]
            con_no = row[5]
            remark = row[6]
            mm = row[7]
            dd = row[8]
            date = row[9]
            enddate = row[10]
            moano = row[12]
            comm = row[13]
            atab = row[14]
            water = row[15]
            Managexp = row[16]
            INSUR = row[17]
            OTHER = row[18]
            ADVANCE = row[19]
            SAL_NO = row[20]
            MONTH = row[21]
            DAY = row[22]
            PAYWAY = row[23]
            CHQNO = row[24]
            user_add = row[25]
            user_edit = row[26]
            rent_no = row[27]
            unitno = row[28]
            BALANCE = row[29]

            DUEBALANCE = row[30]
            REMARKS = row[31]
            CASHED = row[32]
            DATECASHED = row[33]
            CASHEDBY = row[34]
            printed = row[35]
            VatRent = row[36]
            VatCom = row[37]
            VatSay = row[38]
            VatOwnerNo = row[39]
            VatRat = row[40]

            remark_str = ""
            if pay_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "PAY_NAME: {0}".format(pay_name)

            if akarno:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "akarno: {0}".format(akarno)
            if con_no:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "CON_NO: {0}".format(con_no)
            if remark:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "REMARK: {0}".format(remark)
            if mm:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "MM: {0}".format(mm)
            if dd:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "DD: {0}".format(dd)
            if date:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "date: {0}".format(date)
            if enddate:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "enddate: {0}".format(enddate)
            if moano:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "MOANO: {0}".format(moano)

            if comm:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "COMM: {0}".format(comm)

            if atab:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "ATAB: {0}".format(atab)
            if water:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "water: {0}".format(water)
            if Managexp:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "Managexp: {0}".format(Managexp)
            if INSUR:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "INSUR: {0}".format(INSUR)

            if OTHER:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "OTHER: {0}".format(OTHER)

            if ADVANCE:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "ADVANCE: {0}".format(ADVANCE)

            if SAL_NO:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "SAL_NO: {0}".format(SAL_NO)
            if MONTH:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "MONTH: {0}".format(MONTH)
            if DAY:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "DAY: {0}".format(DAY)
            if PAYWAY:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "PAYWAY: {0}".format(PAYWAY)
            if CHQNO:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "CHQNO: {0}".format(CHQNO)
            if user_add:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "user_add: {0}".format(user_add)
            if user_edit:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "user_edit: {0}".format(user_edit)
            if rent_no:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "rent_no: {0}".format(rent_no)
            if unitno:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "unitno: {0}".format(unitno)
            if BALANCE:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "BALANCE: {0}".format(BALANCE)
            if DUEBALANCE:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "DUEBALANCE: {0}".format(DUEBALANCE)
            if REMARKS:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "REMARKS: {0}".format(REMARKS)
            if CASHED:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "CASHED: {0}".format(CASHED)
            if DATECASHED:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "DATECASHED: {0}".format(DATECASHED)
            if CASHEDBY:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "rent_no: {0}".format(CASHEDBY)
            if printed:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "printed: {0}".format(printed)
            if VatRent:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "VatRent: {0}".format(VatRent)
            if VatCom:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "VatCom: {0}".format(VatCom)
            if VatSay:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "VatSay: {0}".format(VatSay)
            if VatOwnerNo:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "VatOwnerNo: {0}".format(VatOwnerNo)
            if VatRat:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "VatRat: {0}".format(VatRat)

            journal_entry = frappe.get_doc(
                dict(
                    doctype="Journal Entry",
                    title=str(serial_no),
                    voucher_type="Journal Entry",
                    naming_series="JV-",
                    posting_date=post_date,
                    company=company.name,
                    user_remark=remark,
                    multi_currency=0,
                    remark=remark_str,
                    bill_date=datetime.now(),
                    third_party_creation=post_date,
                    accounts=[],
                    is_opening="No",
                    cheque_no=CHQNO,
                    cheque_date=post_date if CHQNO else None
                )
            )

            journal_entry.append("accounts", dict(
                account=from_account,
                against_account=to_account,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=abs(amount),
                debit=abs(amount),
                journal_note=remark,
                credit_in_account_currency=abs(0),
                credit=abs(0),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.append("accounts", dict(
                party_type="Company",
                party=company.name,
                account=to_account,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=0,
                debit=0,
                journal_note=remark,
                credit_in_account_currency=abs(amount),
                credit=abs(amount),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.flags.ignore_permissions = True

            journal_entry.submit()

            print journal_entry.name
            frappe.db.commit()

    print("Done payment..")
    frappe.db.commit()


def execute():
    payment_details = "/private/files/payment_details.csv"
    payment = "/private/files/payment.csv"
    owners = "/private/files/owners.csv"
    parent_account = "50101 - حسابات الدائنون - N"
    print("Starting owners..")
    current_file = get_file_path(owners)
    company = frappe.get_doc(
        "Company",
        dict(
            company_name="Nahdi"
        )
    )
    main_cost_center = frappe.get_value(
        "Cost Center",
        dict(
            company=company.name,
            parent_cost_center=None
        ),
        "name"
    )

    cash_account = "3030601 - نقد - N"
    # with open(current_file, 'rb') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
    #     for row in spamreader:
    #         # print row
    #         try:
    #             serial_no = int(row[0])
    #         except:
    #             continue
    #         name = str(row[1])
    #
    #         doc = frappe.get_doc(
    #             dict(
    #                 doctype="Account",
    #                 account_name="{0} - {1}".format(serial_no, name),
    #                 account_number=None,
    #                 company=company.name,
    #                 is_group=0,
    #                 # account_currency="SAR",
    #                 parent_account=parent_account,
    #                 report_type="Balance Sheet"
    #             )
    #         )
    #         doc.flags.ignore_mandatory = True
    #         doc.insert(ignore_permissions=True)
    #
    # print("Done owners..")
    # frappe.db.commit()
    # print("Start Payments..")
    # current_file = get_file_path(payment)
    #
    # with open(current_file, 'rb') as csvfile:
    #     spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
    #     for row in spamreader:
    #         # print row
    #         try:
    #             serial_no = int(row[0])
    #         except:
    #             continue
    #
    #         post_date = row[1]
    #         post_date = datetime.strptime(
    #             str(post_date), '%Y/%m/%d'
    #         )
    #         account_no = str(row[2])
    #         value_1 = float(row[3])
    #         value_2 = float(row[4])
    #         value_3 = float(row[5])
    #         value_4 = float(row[6])
    #         cheq = str(row[7])
    #         bank = str(row[8])
    #         remark = str(row[9])
    #         pay_name = str(row[10])
    #         receipt_no = str(row[11])
    #         total = value_1 + value_2 + value_3 + value_4
    #         remark_str = ""
    #         if cheq:
    #             remark_str = remark_str + "CHEQNO: {0}".format(cheq)
    #         if bank:
    #             if remark_str:
    #                 remark_str += ", "
    #             remark_str = remark_str + "BANK: {0}".format(bank)
    #         if remark:
    #             if remark_str:
    #                 remark_str += ", "
    #             remark_str = remark_str + "REMARK: {0}".format(remark)
    #         if pay_name:
    #             if remark_str:
    #                 remark_str += ", "
    #             remark_str = remark_str + "PAY_NAME: {0}".format(pay_name)
    #         if receipt_no:
    #             if remark_str:
    #                 remark_str += ", "
    #             remark_str = remark_str + "RCP_NO: {0}".format(receipt_no)
    #         # print(str(account_no))
    #         account_name = frappe.get_value(
    #             "Account",
    #             dict(
    #                 parent_account=parent_account,
    #                 name=("like", "{0} -%".format(account_no))
    #             )
    #         )
    #
    #         if not account_name:
    #             doc = frappe.get_doc(
    #                             dict(
    #                                 doctype="Account",
    #                                 account_name="{0} - مالك رقم {0}".format(account_no),
    #                                 account_number=None,
    #                                 company=company.name,
    #                                 is_group=0,
    #                                 # account_currency="SAR",
    #                                 parent_account=parent_account,
    #                                 report_type="Balance Sheet"
    #                             )
    #                         )
    #             doc.flags.ignore_mandatory = True
    #             doc.insert(ignore_permissions=True)
    #             account_name = doc.name
    #         prev = frappe.get_value(
    #             "Journal Entry",
    #             dict(
    #
    #                 title=str(serial_no)
    #             ),
    #             "name"
    #         )
    #         if int(serial_no) < 34441 and prev:
    #             pass
    #             # frappe.db.set_value(
    #             #     "Journal Entry",
    #             #     prev,
    #             #     "remark",
    #             #     remark_str
    #             # )
    #         else:
    #             journal_entry = frappe.get_doc(
    #                 dict(
    #                     doctype="Journal Entry",
    #                     title=str(serial_no),
    #                     voucher_type="Journal Entry",
    #                     naming_series="JV-",
    #                     posting_date=post_date,
    #                     company=company.name,
    #                     user_remark=remark,
    #                     multi_currency=0,
    #                     remark=remark_str,
    #                     bill_date=datetime.now(),
    #                     third_party_creation=post_date,
    #                     accounts=[],
    #                     is_opening="No",
    #                     cheque_no=cheq,
    #                     cheque_date=post_date if cheq else None
    #                 )
    #             )
    #
    #             journal_entry.append("accounts", dict(
    #                 account=cash_account,
    #                 against_account=account_name,
    #                 title=remark,
    #                 exchange_rate=1,
    #                 debit_in_account_currency=abs(total),
    #                 debit=abs(total),
    #                 journal_note=remark,
    #                 credit_in_account_currency=abs(0),
    #                 credit=abs(0),
    #                 is_advance="No",
    #                 cost_center=main_cost_center
    #             ))
    #             journal_entry.append("accounts", dict(
    #                 party_type="Company",
    #                 party=company.name,
    #                 account=account_name,
    #                 title=remark,
    #                 exchange_rate=1,
    #                 debit_in_account_currency=0,
    #                 debit=0,
    #                 journal_note=remark,
    #                 credit_in_account_currency=abs(total),
    #                 credit=abs(total),
    #                 is_advance="No",
    #                 cost_center=main_cost_center
    #             ))
    #             journal_entry.flags.ignore_permissions = True
    #
    #             journal_entry.submit()
    #
    #             print journal_entry.name
    #         frappe.db.commit()
    #
    # print("Done payment..")
    # frappe.db.commit()

    print("Start Payments details..")
    current_file = get_file_path(payment_details)
    counter = 1
    with open(current_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=str(","), quotechar=str("|"))
        for row in spamreader:
            # print row
            if row[0]:
                try:
                    serial_no = int(row[0])
                except:
                    continue
            else:
                pass
            if not row[1]:
                continue
            serial_no = "{:06d}".format(counter)
            if frappe.db.exists(
                "Journal Entry",
                dict(
                    title=str(serial_no)
                )
            ):
                counter += 1
                continue
            counter += 1
            post_date = row[1]
            post_date = datetime.strptime(
                str(post_date), '%Y/%m/%d'
            )
            total = float(row[2])

            account_no = str(row[3])
            pay_no = str(row[4])
            serialno = str(row[5])
            remark = str(row[6])
            moa_no_name = str(row[7])
            pay_name = str(row[8])
            akar_no = str(row[9])
            akar_address = str(row[10])

            remark_str = ""
            if pay_no:
                remark_str = remark_str + "PAY_NO: {0}".format(pay_no)
            if serialno:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "SerialNo: {0}".format(serialno)
            if remark:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "REMARK: {0}".format(remark)
            if moa_no_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "MoaNoName: {0}".format(moa_no_name)
            if pay_name:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "PAY_NAME: {0}".format(pay_name)
            if akar_no:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "AKAR_NO: {0}".format(akar_no)
            if akar_address:
                if remark_str:
                    remark_str += ", "
                remark_str = remark_str + "AKAR_ADDRESS: {0}".format(akar_address)

            account_name = frappe.get_value(
                "Account",
                dict(
                    parent_account=parent_account,
                    name=("like", "{0} -%".format(account_no))
                )
            )
            journal_entry = frappe.get_doc(
                dict(
                    doctype="Journal Entry",
                    title=str(serial_no),
                    voucher_type="Journal Entry",
                    naming_series="JV-",
                    posting_date=post_date,
                    company=company.name,
                    user_remark=remark,
                    multi_currency=0,
                    remark=remark_str,
                    bill_date=datetime.now(),
                    third_party_creation=post_date,
                    accounts=[],
                    is_opening="No"
                )
            )

            journal_entry.append("accounts", dict(
                account=cash_account,
                against_account=account_name,
                party_type=None,
                party=None,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=abs(total),
                debit=abs(total),
                journal_note=remark,
                credit_in_account_currency=abs(0),
                credit=abs(0),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.append("accounts", dict(
                account=account_name,
                party_type="Company",
                party=company.name,
                title=remark,
                exchange_rate=1,
                debit_in_account_currency=0,
                debit=0,
                journal_note=remark,
                credit_in_account_currency=abs(total),
                credit=abs(total),
                is_advance="No",
                cost_center=main_cost_center
            ))
            journal_entry.flags.ignore_permissions = True

            journal_entry.submit()

            print journal_entry.name
            frappe.db.commit()

    print("Done payment details..")
    frappe.db.commit()
