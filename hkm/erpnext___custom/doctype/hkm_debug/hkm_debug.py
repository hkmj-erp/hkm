# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class HKMDebug(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        data: DF.LongText | None
        document_name: DF.DynamicLink | None
        document_type: DF.Link
        ip: DF.Data | None
    # end: auto-generated types
    pass


@frappe.whitelist()
def add_debug_entry(doctype, data, name=None):
    doc = frappe.get_doc(
        {
            "doctype": "HKM Debug",
            "document_type": doctype,
            "data": data,
            "document_name": name,
            "ip": frappe.local.request_ip,
        }
    )
    doc.insert(ignore_permissions=True)
