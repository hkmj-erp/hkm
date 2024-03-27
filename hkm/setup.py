import frappe, click
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields


def after_install():
    frappe.clear_cache()


def make_custom_fields(update=True):
    pass


def get_custom_fields():
    pass
