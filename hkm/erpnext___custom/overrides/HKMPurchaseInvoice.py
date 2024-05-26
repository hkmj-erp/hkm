# Copyright (c) 2021, Tara Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
from erpnext.accounts.doctype.purchase_invoice.purchase_invoice import PurchaseInvoice
import frappe
from frappe import _, throw
from frappe.utils import flt
from frappe.utils.data import getdate
from frappe.model.naming import getseries


class HKMPurchaseInvoice(PurchaseInvoice):
    def autoname(self):
        dateF = getdate(self.posting_date)
        company_abbr = frappe.get_cached_value("Company", self.company, "abbr")
        year = dateF.strftime("%y")
        month = dateF.strftime("%m")
        prefix = f"{company_abbr}-PI-{year}{month}-"
        self.name = prefix + getseries(prefix, 5)
