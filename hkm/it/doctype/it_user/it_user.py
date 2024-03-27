# -*- coding: utf-8 -*-
# Copyright (c) 2021, NRHD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class ITUser(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		department: DF.Link | None
		email: DF.Data | None
		frappe_user: DF.Link | None
		mobile: DF.Data | None
		name1: DF.Data
		naming_series: DF.Literal["ITU-"]
		type: DF.Literal["Devotee", "Employee"]
	# end: auto-generated types
	pass
