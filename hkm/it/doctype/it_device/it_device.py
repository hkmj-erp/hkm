# -*- coding: utf-8 -*-
# Copyright (c) 2021, NRHD and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
# import frappe
from frappe.model.document import Document

class ITDevice(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF
		from hkm.it.doctype.it_device_specification.it_device_specification import ITDeviceSpecification

		age: DF.Data | None
		bill: DF.Attach | None
		brand: DF.Link | None
		category: DF.Link | None
		company: DF.Link
		image: DF.AttachImage | None
		it_user: DF.Link | None
		location: DF.Data | None
		model: DF.Data | None
		naming_series: DF.Literal["ITD-.YY.-"]
		password: DF.Data | None
		purchase_cost: DF.Currency
		purchase_date: DF.Date | None
		specifications: DF.Table[ITDeviceSpecification]
		status: DF.Literal[None]
	# end: auto-generated types
	pass
