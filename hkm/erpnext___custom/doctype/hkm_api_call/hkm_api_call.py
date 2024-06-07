# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document


class HKMAPICall(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        api_data: DF.JSON | None
        path: DF.Data | None
        request_ip: DF.Data | None
        user: DF.Link | None
    # end: auto-generated types
    pass


@frappe.whitelist()
def store_incoming_api():
    received_data = json.loads(frappe.request.data)
    doc = frappe.get_doc(
        {
            "doctype": "HKM API Call",
            "user": frappe.session.user,
            "request_ip": frappe.local.request_ip,
            "api_data": received_data,
            # "headers": frappe.request.headers,
            "path": frappe.request.path,
        }
    )
    doc.insert(ignore_permissions=True)
