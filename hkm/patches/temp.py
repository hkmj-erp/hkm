import frappe


def execute():
    frappe.db.set_value(
        "Dhananjaya Settings",
        "Dhananjaya Settings",
        "cash_cheque_collection_channel",
        "Dhananjaya-Cash Cheque Collection",
    )
    frappe.db.commit()
