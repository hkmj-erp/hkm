import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def execute():
    custom_fields = {
        "Stock Entry": [
            dict(
                fieldname="default_difference_account",
                label="Default Difference Account",
                fieldtype="Link",
                options="Account",
                insert_after="source_address_display",
                translatable=0,
                mandatory_depends_on="eval:doc.purpose=='Material Issue' || doc.purpose=='Material Receipt'",
            ),
            dict(
                fieldname="default_difference_cost_center",
                label="Default Cost Center",
                fieldtype="Link",
                options="Cost Center",
                insert_after="default_difference_account",
                translatable=0,
                mandatory_depends_on="eval:doc.purpose=='Material Issue' || doc.purpose=='Material Receipt'",
            ),
        ],
        "Purchase Invoice": [
            dict(
                fieldname="default_difference_account",
                label="Default Difference Account",
                fieldtype="Link",
                options="Account",
                insert_after="items_section",
                translatable=0,
            ),
            dict(
                fieldname="default_difference_cost_center",
                label="Default Cost Center",
                fieldtype="Link",
                options="Cost Center",
                insert_after="default_difference_account",
                translatable=0,
                reqd=1,
            ),
        ],
        "Sales Invoice": [
            dict(
                fieldname="default_sales_income_account",
                label="Default Sales Income Account",
                fieldtype="Link",
                options="Account",
                insert_after="items_section",
                translatable=0,
            ),
            dict(
                fieldname="default_difference_cost_center",
                label="Default Cost Center",
                fieldtype="Link",
                options="Cost Center",
                insert_after="default_sales_income_account",
                mandatory_depends_on="eval:!doc.is_pos",
                translatable=0,
            ),
        ],
    }
    create_custom_fields(custom_fields)
