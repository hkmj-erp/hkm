# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, timedelta
from frappe.model.document import Document


class HKMRedirect(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        ephemeral: DF.Check
        redirect_to: DF.Data | None
    # end: auto-generated types
    pass


def delete_temporary_short_links():
    three_days_ago = (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d")
    eligible_links = frappe.get_all(
        "HKM Redirect",
        filters=[["creation", "<", three_days_ago], ["ephemeral", "=", 1]],
        page_length=300,
        order_by="creation",
        pluck="name",
    )
    for link in eligible_links:
        frappe.delete_doc("HKM Redirect", link)
