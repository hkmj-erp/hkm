import frappe
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils.data import cstr


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
                fieldname="cost_center",
                label="Cost Center",
                fieldtype="Link",
                options="Cost Center",
                reqd=1,
                insert_after="project",
                translatable=0,
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
        ],
    }
    create_custom_fields(custom_fields)

    custom_field = "default_difference_cost_center"
    for doctype in ["Purchase Invoice", "Sales Invoice", "Stock Entry"]:
        frappe.db.delete(
            "Custom Field",
            {
                "fieldname": custom_field,
                "dt": doctype,
            },
        )
        frappe.clear_cache(doctype=doctype)


# def execute():
#     site_name = cstr(frappe.local.site)
#     if site_name == "hkmjerp.in":
#         return
#     custom_fields = [
#         "ka_head",
#         "folk_residency",
#         "cashier_received_the_money",
#         "to_other_company",
#         "is_issue_to_another_company",
#     ]
#     for doctype in ["Purchase Invoice", "Sales Invoice", "Stock Entry"]:
#         frappe.db.delete(
#             "Custom Field",
#             {
#                 "fieldname": ("in", [field for field in custom_fields]),
#                 "dt": doctype,
#             },
#         )
#     custom_properties = [
#         "default_print_format",
#     ]
#     for doctype in ["Purchase Invoice", "Sales Invoice", "Stock Entry"]:
#         frappe.db.delete(
#             "Property Setter",
#             {
#                 "property": ("in", [field for field in custom_properties]),
#                 "doc_type": doctype,
#             },
#         )
#     frappe.clear_cache(doctype=doctype)


def execute():
    custom_fields = {
        "Stock Entry": [
            dict(
                fieldname="ka_head",
                label="KA Head",
                fieldtype="Link",
                options="KA Head",
                insert_after="project",
                translatable=0,
            ),
        ]
    }
    create_custom_fields(custom_fields)
