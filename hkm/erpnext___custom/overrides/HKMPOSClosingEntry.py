import frappe
from erpnext.accounts.doctype.pos_closing_entry.pos_closing_entry import POSClosingEntry
from frappe.model.naming import getseries
from datetime import timedelta, datetime
from frappe.utils.data import get_datetime


class HKMPOSClosingEntry(POSClosingEntry):
    def validate(self):
        super().validate()
        self.validate_all_pos_included()

    def validate_all_pos_included(self):
        count = frappe.db.sql(
            f"""
                        SELECT COUNT(*)
                        FROM `tabPOS Invoice`
                        WHERE
                            status = 'Paid'
                            and docstatus = 1
                            and pos_profile = '{self.pos_profile}'
                            and creation >= '{get_datetime(self.period_start_date).strftime("%Y-%m-%d %H:%M:00")}'
                            and creation <= '{get_datetime(self.period_end_date).strftime("%Y-%m-%d %H:%M:59")}'
                        """
        )[0][0]

        if count != len(self.pos_transactions):
            frappe.throw(
                "All the POS Invoices from start time to end time are not included. The reason could be that you are immediately closing the POS after the last POS Invoice."
            )
        return
