import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    custom_fields = {
        "Journal Entry": [
            dict(
                fieldname="bank_statement_name",
                label="Bank Statement",
                fieldtype="Data",
                insert_after="tax_withholding_category",
                translatable=0,
                read_only=1,
            ),
        ],
        "Payment Entry": [
            dict(
                fieldname="bank_statement_name",
                label="Bank Statement",
                fieldtype="Data",
                insert_after="references",
                translatable=0,
                read_only=1,
            ),
        ],
    }
    create_custom_fields(custom_fields)
