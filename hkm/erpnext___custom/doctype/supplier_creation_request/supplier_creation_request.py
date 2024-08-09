# Copyright (c) 2022, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.mapper import get_mapped_doc


class SupplierCreationRequest(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        aadhar_no: DF.Data | None
        address_line_1: DF.Data
        address_line_2: DF.Data | None
        bank: DF.Link | None
        bank_account_name: DF.Data | None
        bank_account_number: DF.Data | None
        bank_branch_code: DF.Data | None
        city: DF.Data
        country: DF.Link
        gstin: DF.Data | None
        mobile_number: DF.Data | None
        pan: DF.Data | None
        pincode: DF.Data
        state: DF.Literal["", "Andaman and Nicobar Islands", "Andhra Pradesh", "Arunachal Pradesh", "Assam", "Bihar", "Chandigarh", "Chhattisgarh", "Dadra and Nagar Haveli and Daman and Diu", "Delhi", "Goa", "Gujarat", "Haryana", "Himachal Pradesh", "Jammu and Kashmir", "Jharkhand", "Karnataka", "Kerala", "Ladakh", "Lakshadweep Islands", "Madhya Pradesh", "Maharashtra", "Manipur", "Meghalaya", "Mizoram", "Nagaland", "Odisha", "Other Territory", "Pondicherry", "Punjab", "Rajasthan", "Sikkim", "Tamil Nadu", "Telangana", "Tripura", "Uttar Pradesh", "Uttarakhand", "West Bengal"]
        supplier_group: DF.Link
        supplier_name: DF.Data
        supplier_type: DF.Literal["Company", "Individual"]
    # end: auto-generated types
    pass


@frappe.whitelist()
def create_supplier(source_name, target_doc=None):
    # def update_item(source, target, source_parent):
    # 	#target.warehouse = source_parent.warehouse

    doclist = get_mapped_doc(
        "Supplier Creation Request",
        source_name,
        {
            "Supplier Creation Request": {
                "doctype": "Supplier",
                "field_map": {
                    "supplier_name": "supplier_name",
                    "supplier_type": "supplier_type",
                    "supplier_creation_request": "name",
                },
            },
        },
        target_doc,
    )

    if hasattr(doclist, "custom_aadhar_no"):
        doclist.custom_aadhar_no = frappe.db.get_value(
            "Supplier Creation Request", source_name, "aadhar_no"
        )

    return doclist
