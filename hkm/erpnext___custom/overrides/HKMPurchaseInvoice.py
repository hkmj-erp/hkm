# Copyright (c) 2021, Tara Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
import datetime

from attr import fields
from pymysql import Date
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
import frappe
from frappe import _, throw
from frappe.model.docstatus import DocStatus
from frappe.utils import flt
from frappe.utils.data import getdate
from frappe.model.naming import getseries


class HKMPurchaseInvoice(PurchaseInvoice):
    def autoname(self):
        dateF = getdate(self.posting_date)
        company_abbr = frappe.get_cached_value("Company", self.company, "abbr")
        year = dateF.strftime("%y")
        month = dateF.strftime("%m")
        prefix = f"{company_abbr}-PI-{year}{month}-"
        self.name = prefix + getseries(prefix, 5)


@frappe.whitelist()
def get_documents_map_data(document):
    doc = frappe.get_doc("Purchase Invoice", document)
    purchase_receipts = []
    purchase_orders = []
    material_requests = []
    for item in doc.items:
        purchase_orders.append(item.purchase_order)
        purchase_receipts.append(item.purchase_receipt)
    purchase_orders = set(purchase_orders)
    purchase_receipts = set(purchase_receipts)
    for po in purchase_orders:
        if not po:
            continue
        requests = frappe.get_all(
            "Purchase Order Item", filters={"parent": po}, pluck="material_request"
        )
        material_requests.extend(requests)
    material_requests = set(material_requests)
    mrn_docs = []
    po_docs = []
    pr_docs = []
    for m in material_requests:
        if not m:
            continue
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_name": m, "attached_to_doctype": "Material Request"},
            fields=["file_url"],
        )
        doc_dict = frappe.get_doc("Material Request", m).as_dict()
        doc_dict.attachments = attachments
        mrn_docs.append(doc_dict)
    for p in purchase_orders:
        if not p:
            continue
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_name": p, "attached_to_doctype": "Purchase Order"},
            fields=["file_url", "file_name"],
        )
        doc_dict = frappe.get_doc("Purchase Order", p).as_dict()
        doc_dict.attachments = attachments
        po_docs.append(doc_dict)
    for p in purchase_receipts:
        if not p:
            continue
        attachments = frappe.get_all(
            "File",
            filters={"attached_to_name": p, "attached_to_doctype": "Purchase Receipt"},
            fields=["file_url", "file_name"],
        )
        doc_dict = frappe.get_doc("Purchase Receipt", p).as_dict()
        doc_dict.attachments = attachments
        pr_docs.append(doc_dict)

    data = frappe._dict(
        material_requests=mrn_docs,
        purchase_orders=po_docs,
        purchase_receipts=pr_docs,
    )
    return frappe.render_template("templates/purchase_invoice/documents_map.html", data)
