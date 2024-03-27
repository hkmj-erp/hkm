# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class FirebaseAppToken(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF

        app: DF.Link | None
        device_id: DF.Data | None
        device_name: DF.Data | None
        token: DF.Data | None
        user: DF.Link | None
    # end: auto-generated types
    pass
