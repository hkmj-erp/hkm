import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    custom_fields = {
        "User": [
            dict(
                fieldname="custom_tab",
                label="Custom",
                fieldtype="Tab Break",
                insert_after="onboarding_status",
                translatable=0,
            ),
            dict(
                fieldname="po_section_break",
                label="Purchase Order",
                fieldtype="Section Break",
                insert_after="custom_tab",
                translatable=0,
            ),
            dict(
                fieldname="purchase_order_whatsapp_approval",
                label="Purchase Order Whatsapp Approval",
                default=1,
                fieldtype="Check",
                insert_after="po_section_break",
                translatable=0,
            ),
        ],
    }
    create_custom_fields(custom_fields)
