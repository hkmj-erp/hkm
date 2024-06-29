from __future__ import unicode_literals
from . import __version__ as app_version
from hkm.erpnext___custom.doctype.user_company_allowed.list_view import (
    get_applicable_documents,
)
from hkm.fixtures import custom_fixtures

app_name = "hkm"
app_title = "Hare Krishna Movement"
app_publisher = "Narahari Dasa"
app_description = "For Various Departments in HKM"
app_icon = "sitemap"
app_color = "blue"
app_email = "nrhd@hkm-group.org"
app_license = "MIT"

export_python_type_annotations = True

# include js, css files in header of desk.html
app_include_css = "hkmj-theme.bundle.css"
app_include_js = "shortcuts.bundle.js"

# include js, css files in header of web template
web_include_css = "hkmj-web.bundle.css"
# web_include_js = "/assets/custom_app/js/custom_app.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "custom_app/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {
# 	"point-of-sale" : "public/js/point_of_sale.js",
# }

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {
    "Material Request": "public/js/material_request.js",
    "Purchase Order": "public/js/purchase_order.js",
    "Journal Entry": "public/js/journal_entry.js",
    "Purchase Receipt": "public/js/purchase_receipt.js",
    "Stock Entry": "public/js/stock_entry.js",
    "Purchase Invoice": "public/js/purchase_invoice.js",
    "Sales Invoice": "public/js/sales_invoice.js",
    "Item": "public/js/item.js",
    "POS Invoice": "public/js/pos_invoice.js",
    "Item Code Printer": "public/js/item_code_printer.js",
    "Bank Transaction": "public/js/bank_transaction.js",
}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

website_route_rules = [
    {"from_route": "/sl/<short_url>", "to_route": "redirect"},
]

website_generators = ["DD User Address"]

# add methods and filters to jinja environment
jinja = {"methods": ["hkm.ahmedabad.custom.get_purchase_order_details"]}


# Installation
# ------------

# before_install = "custom_app.install.before_install"
after_install = "hkm.erpnext___custom.setup.after_install"
before_uninstall = "hkm.erpnext___custom.setup.before_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "custom_app.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

permission_query_conditions = {
    "FOLK Student": "hkm.folk_base.folk_listview_filter.student_query",
    "Ashraya Candidate": "hkm.ashraya_base.ashraya_listview_filter.query",
    "DD Wallet Tx": "hkm.divine_dishes.list_view_filter.query",
    "DD Subscription": "hkm.divine_dishes.list_view_filter.query",
    "DD Order": "hkm.divine_dishes.list_view_filter.query",
}

# For Company Filters for Particular Users
documents = get_applicable_documents()

permission_query_conditions.update(
    dict.fromkeys(
        documents, "hkm.erpnext___custom.doctype.user_company_allowed.list_view.query"
    )
)
permission_query_conditions.update(
    {
        "Company": "hkm.erpnext___custom.doctype.user_company_allowed.list_view.company_specific"
    }
)

#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }
override_doctype_class = {
    "POS Invoice": "hkm.erpnext___custom.overrides.HKMPOSInvoice.HKMPOSInvoice",
    "POS Closing Entry": "hkm.erpnext___custom.overrides.HKMPOSClosingEntry.HKMPOSClosingEntry",
    "Sales Invoice": "hkm.erpnext___custom.overrides.HKMSalesInvoice.HKMSalesInvoice",
    "Journal Entry": "hkm.erpnext___custom.overrides.HKMJournalEntry.HKMJournalEntry",
    "Material Request": "hkm.erpnext___custom.overrides.HKMMaterialRequest.HKMMaterialRequest",
    "Purchase Order": "hkm.erpnext___custom.overrides.purchase_order.HKMPurchaseOrder.HKMPurchaseOrder",
    "Purchase Invoice": "hkm.erpnext___custom.overrides.HKMPurchaseInvoice.HKMPurchaseInvoice",
    "Payment Entry": "hkm.erpnext___custom.overrides.HKMPaymentEntry.HKMPaymentEntry",
}

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
    "*": {
        "before_insert": "hkm.erpnext___custom.doctype.freeze_transaction_settings.freeze_transaction_settings.validate_transaction_against_frozen_date",
        "before_cancel": "hkm.erpnext___custom.doctype.freeze_transaction_settings.freeze_transaction_settings.validate_transaction_against_frozen_date",
        "before_save": "hkm.erpnext___custom.letterhead.letterhead_query",
    },
    "Task": {"on_update": "hkm.erpnext___custom.task_notification.query"},
    "Sales Invoice": {
        # "validate": "hkm.erpnext___custom.overrides.sales_invoice.validate_extra",
        "before_submit": "hkm.erpnext___custom.extend.accounts_controller.validate_gst_entry",
    },
    "Supplier": {
        "before_insert": "hkm.erpnext___custom.extend.supplier.creation_from_gstin",
        "on_update": "hkm.erpnext___custom.extend.supplier.fetch_address_from_creation_request",
    },
    "Item": {
        "before_insert": "hkm.erpnext___custom.extend.item.item_taxes_and_income_account_set",  # Before the document first time inserted, this will not run always whenever some changes are made to the document
        "before_insert": "hkm.erpnext___custom.extend.item.update_item_code_in_barcodes",
        "after_insert": "hkm.erpnext___custom.extend.item.item_creation_update",
    },
    "Purchase Invoice": {
        "before_submit": [
            "hkm.erpnext___custom.extend.accounts_controller.validate_expense_account_for_non_stock_item",
            "hkm.erpnext___custom.extend.accounts_controller.validate_gst_entry",
        ],
    },
    "Stock Entry": {
        "before_submit": "hkm.erpnext___custom.extend.accounts_controller.validate_expense_account_for_non_stock_item",
        "before_insert": "hkm.erpnext___custom.doctype.mrn_usability_settings.mrn_usability_settings.validate_mrn_settings",
    },
    "Purchase Receipt": {
        "validate": "hkm.erpnext___custom.extend.purchase_receipt.validate",
    },
}
# Scheduled Tasks
# ---------------
scheduler_events = {
    "daily_long": [
        "hkm.erpnext___custom.doctype.hkm_redirect.hkm_redirect.delete_temporary_short_links",
        "hkm.firebase.doctype.app_notification.app_notification.delete_old_app_notifications",
    ],
    "cron": {"15 20 * * *": ["hkm.divine_dishes.tasks.every_day_evening"]},
}

# scheduler_events = {
# 	"cron": {
#        "monthly": [
#            "hkm.erpnext___custom.item.unused_item_code_disable"
#        ]
#    }
# 	"all": [
# 		"custom_app.tasks.all"
# 	],
# 	"daily": [
# 		"custom_app.tasks.daily"
# 	],
# "hourly": [
# 	"custom_app.modification.hr_attendance_fetch.fetch"
# ]
# 	"weekly": [
# 		"custom_app.tasks.weekly"
# 	]
# 	"monthly": [
# 		"custom_app.tasks.monthly"
# 	]
# "cron": {
#        "30 23 * * *": [
#            "custom_app.modification.hr_attendance_fetch.fetch"
#        ]
#    }
# }

# Testing
# -------

# before_tests = "custom_app.install.before_tests"

# fixtures = [
# "Custom Field",
# "Custom DocPerm",
# "Devotee",
# "Buying Settings",
# "Selling Settings",
# "Stock Settings",
# "HR Settings",
# "System Settings",
# "Payroll Settings",
# "Accounts Settings",
# "List View Settings",
# "Portal Settings",
# # Ashram
# "Ashram Library Book",
# "Ashram Store Item",
# # HR
# "Salutation",
# "Designation",
# "Employee Grade",
# # Store
# "UOM",
# # Misc
# "Role",
# "Custom DocPerm",
# "Role Profile",
# "Workflow State",
# "Workflow",
# "Client Script"
# "Item Group",
# "GST HSN Code",
# "Role",
# "Item Attribute"
# "Supplier Group",
# {"doctype": "Address", "filters": [
#     [
#         "city", "like", "%udaipur%"
#     ]
# ]},
# {"doctype": "Supplier", "filters": [
#     [
#         "primary_address", "like", "%udaipur%"
#     ]
# ]},
# {"doctype": "Cost Center", "filters": [
#     [
#         "company", "=","Kota - Hare Krishna Movement"
#     ]
# ]},
# "Role","Custom DocPerm","Property Setter"
# "DocType Link"
# ]

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "custom_app.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "custom_app.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
    {
        "doctype": "{doctype_1}",
        "filter_by": "{filter_by}",
        "redact_fields": ["{field_1}", "{field_2}"],
        "partial": 1,
    },
    {
        "doctype": "{doctype_2}",
        "filter_by": "{filter_by}",
        "partial": 1,
    },
    {
        "doctype": "{doctype_3}",
        "strict": False,
    },
    {"doctype": "{doctype_4}"},
]

fixtures = custom_fixtures

website_route_rules = [
    {"from_route": "/sl/<short_url>", "to_route": "redirect"},
]
