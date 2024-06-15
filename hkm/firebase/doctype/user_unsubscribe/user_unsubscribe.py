# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class UserUnsubscribe(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		channel: DF.Link
		user: DF.Link
	# end: auto-generated types
	def validate(self):
		if frappe.db.exists("User Unsubscribe", {"user": self.user, "channel": self.channel}):
			frappe.throw(frappe._("User '{0}' already unsubscribed from '{1}'").format(self.user, self.channel))
		return
