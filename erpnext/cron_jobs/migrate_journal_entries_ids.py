import frappe


def execute(company_name=None, prefix=None):

    # related_journals = [
    #     ['NA0000002', 'NA0000001-1'],
    #     ['NA0000003', 'NA0000001-2'],
    #     ['MA0000013', 'MA0000012-1'],
    #     ['ANA0000074', 'ANA0000047-1'],
    #     ['ANA0000079', 'ANA0000035-1'],
    #     ['ANA0000112', 'ANA0000085-1'],
    #     ['ANA0000143', 'ANA0000142-1'],
    #     ['ANA0000162', 'ANA0000161-1'],
    #     ['ANA0000191', 'ANA0000144-1'],
    #     ['ANA0000249', 'ANA0000140-1'],
    #     ['ANA0000250', 'ANA0000209-1']
    # ]
    #
    # for journal in related_journals:
    #     old_name = journal[0]
    #     new_name = journal[1]
    #     print old_name,",",new_name
    #     frappe.db.sql("""UPDATE `tabJournal Entry` SET name = %(new_name)s WHERE name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabJournal Entry Account` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabJournal Entry Account` SET parent = %(new_name)s WHERE parent = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabPayment Reconciliation Invoice` SET invoice_number = %(new_name)s WHERE invoice_number = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabDepreciation Schedule` SET journal_entry = %(new_name)s WHERE journal_entry = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabSalary Slip` SET journal_entry = %(new_name)s WHERE journal_entry = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabJournal Entry` SET amended_from = %(new_name)s WHERE amended_from = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabStock Entry` SET credit_note = %(new_name)s WHERE credit_note = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabGL Entry` SET against_voucher = %(new_name)s WHERE against_voucher = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabGL Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabBank Reconciliation Detail` SET payment_entry = %(new_name)s WHERE payment_entry = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabStock Ledger Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabPurchase Invoice Advance` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabSales Invoice Advance` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabPayment Entry Reference` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabPayment Request` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabSubscription` SET reference_document = %(new_name)s WHERE reference_document = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabPatient Medical Record` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabMaintenance Visit Purpose` SET prevdoc_docname = %(new_name)s WHERE prevdoc_docname = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabAuthorization Rule` SET master_name = %(new_name)s WHERE master_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabLanded Cost Item` SET receipt_document = %(new_name)s WHERE receipt_document = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabLanded Cost Purchase Receipt` SET receipt_document = %(new_name)s WHERE receipt_document = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabQuality Inspection` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabSerial No` SET purchase_document_no = %(new_name)s WHERE purchase_document_no = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabSerial No` SET delivery_document_no = %(new_name)s WHERE delivery_document_no = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    #
    #     frappe.db.sql("""UPDATE `tabStock Ledger Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
    #         old_name=old_name,
    #         new_name=new_name
    #     ))
    # frappe.db.commit()
    #
    # return
    if company_name:
        companies = [dict(name=company_name)]
    elif prefix:
         companies = [dict(name=frappe.get_value("Company", dict(prefix=prefix), "name"))]

    else:
        companies = frappe.get_list(
            "Company",
            dict()
        )

    for company in companies:
        print company
        company_name = company['name']
        prefix = frappe.get_value("Company", company_name, "series_prefix")
        if not prefix: continue
        frappe.db.sql("""DELETE FROM tabSeries WHERE name = %(prefix)s""", dict(
            prefix=prefix
        ))
        journals = frappe.db.sql(
            """SELECT name
            FROM `tabJournal Entry`
            WHERE company = %(company)s
            ORDER by creation ASC;""", dict(company=company_name), as_dict=True
        )
        change_log = dict()
        for journal in journals:
            old_name = journal.name
            if "-" in old_name:
                parent_id = old_name.split("-")[0]
                new_name = change_log.get(parent_id) + "-" + old_name.split("-")[1]
            else:
                new_name = _make_autoname(key='{prefix}.#######'.format(prefix=prefix))
            print old_name,",",new_name
            change_log[old_name] = new_name
            frappe.db.sql("""UPDATE `tabJournal Entry` SET name = %(new_name)s WHERE name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Journal Entry",
            #     old_name,
            #     "name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabJournal Entry Account` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Journal Entry Account",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabJournal Entry Account` SET parent = %(new_name)s WHERE parent = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Journal Entry Account",
            #     dict(
            #         parent=old_name
            #     ),
            #     "parent",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabPayment Reconciliation Invoice` SET invoice_number = %(new_name)s WHERE invoice_number = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "Payment Reconciliation Invoice",
            #     dict(
            #         invoice_number=old_name
            #     ),
            #     "invoice_number",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabDepreciation Schedule` SET journal_entry = %(new_name)s WHERE journal_entry = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "Depreciation Schedule",
            #     dict(
            #         journal_entry=old_name
            #     ),
            #     "journal_entry",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabSalary Slip` SET journal_entry = %(new_name)s WHERE journal_entry = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Salary Slip",
            #     dict(
            #         journal_entry=old_name
            #     ),
            #     "journal_entry",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabJournal Entry` SET amended_from = %(new_name)s WHERE amended_from = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Journal Entry",
            #     dict(
            #         amended_from=old_name
            #     ),
            #     "amended_from",
            #     new_name,
            #     update_modified=False
            # )

            frappe.db.sql("""UPDATE `tabStock Entry` SET credit_note = %(new_name)s WHERE credit_note = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "Stock Entry",
            #     dict(
            #         credit_note=old_name
            #     ),
            #     "credit_note",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabGL Entry` SET against_voucher = %(new_name)s WHERE against_voucher = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "GL Entry",
            #     dict(
            #         against_voucher=old_name
            #     ),
            #     "against_voucher",
            #     new_name,
            #     update_modified=False
            # )

            frappe.db.sql("""UPDATE `tabGL Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "GL Entry",
            #     dict(
            #         voucher_no=old_name
            #     ),
            #     "voucher_no",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabBank Reconciliation Detail` SET payment_entry = %(new_name)s WHERE payment_entry = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))

            # frappe.db.set_value(
            #     "Bank Reconciliation Detail",
            #     dict(
            #         payment_entry=old_name
            #     ),
            #     "payment_entry",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabStock Ledger Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Stock Ledger Entry",
            #     dict(
            #         voucher_no=old_name
            #     ),
            #     "voucher_no",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabPurchase Invoice Advance` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Purchase Invoice Advance",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabSales Invoice Advance` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Sales Invoice Advance",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabPayment Entry Reference` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Payment Entry Reference",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )

            # frappe.db.set_value(
            #     "Payment Reconciliation",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )

            frappe.db.sql("""UPDATE `tabPayment Request` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Payment Request",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabSubscription` SET reference_document = %(new_name)s WHERE reference_document = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Subscription",
            #     dict(
            #         reference_document=old_name
            #     ),
            #     "reference_document",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabPatient Medical Record` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Patient Medical Record",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabMaintenance Visit Purpose` SET prevdoc_docname = %(new_name)s WHERE prevdoc_docname = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Maintenance Visit Purpose",
            #     dict(
            #         prevdoc_docname=old_name
            #     ),
            #     "prevdoc_docname",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabAuthorization Rule` SET master_name = %(new_name)s WHERE master_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Authorization Rule",
            #     dict(
            #         master_name=old_name
            #     ),
            #     "master_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabLanded Cost Item` SET receipt_document = %(new_name)s WHERE receipt_document = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Landed Cost Item",
            #     dict(
            #         receipt_document=old_name
            #     ),
            #     "receipt_document",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabLanded Cost Purchase Receipt` SET receipt_document = %(new_name)s WHERE receipt_document = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Landed Cost Purchase Receipt",
            #     dict(
            #         receipt_document=old_name
            #     ),
            #     "receipt_document",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabQuality Inspection` SET reference_name = %(new_name)s WHERE reference_name = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Quality Inspection",
            #     dict(
            #         reference_name=old_name
            #     ),
            #     "reference_name",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabSerial No` SET purchase_document_no = %(new_name)s WHERE purchase_document_no = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Serial No",
            #     dict(
            #         purchase_document_no=old_name
            #     ),
            #     "purchase_document_no",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabSerial No` SET delivery_document_no = %(new_name)s WHERE delivery_document_no = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Serial No",
            #     dict(
            #         delivery_document_no=old_name
            #     ),
            #     "delivery_document_no",
            #     new_name,
            #     update_modified=False
            # )
            frappe.db.sql("""UPDATE `tabStock Ledger Entry` SET voucher_no = %(new_name)s WHERE voucher_no = %(old_name)s;""", dict(
                old_name=old_name,
                new_name=new_name
            ))
            # frappe.db.set_value(
            #     "Stock Ledger Entry",
            #     dict(
            #         voucher_no=old_name
            #     ),
            #     "voucher_no",
            #     new_name,
            #     update_modified=False
            # )
        frappe.db.commit()


def _make_autoname(key='Agent.-.#####', year=None):
    from frappe.model.naming import getseries
    from frappe.utils import now_datetime
    parts = key.split('.')
    n = ''
    for e in parts:
        if e.startswith('#'):
            digits = len(e)
            part = getseries(n, digits, "")
        elif e == 'YYYY':
            if year:
                part = str(year)
            else:
                part = now_datetime().strftime('%Y')
        else:
            part = e

        n += part
    return n