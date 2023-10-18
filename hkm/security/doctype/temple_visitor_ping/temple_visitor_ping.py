# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

from datetime import datetime
import frappe
from frappe.model.document import Document
from frappe.utils.data import today


class TempleVisitorPing(Document):
    pass


@frappe.whitelist()
def get_today_count():
    return frappe.get_all(
        "Temple Visitor Ping",
        fields=["sum(count) as count"],
        filters=[["date", "=", datetime.today().strftime("%Y-%m-%d")]],
        group_by="date",
    )[0]["count"]
