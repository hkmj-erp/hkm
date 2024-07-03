import frappe
from erpnext.accounts.doctype.sales_invoice.sales_invoice import SalesInvoice
from frappe.utils.data import getdate
from frappe.model.naming import getseries
from datetime import timedelta, date


class HKMSalesInvoice(SalesInvoice):
    def validate(self):
        super().validate()
        self.validate_if_zero_rate_item()
        self.validate_back_dated_entry()

    def autoname(self):
        # select a project name based on customer
        dateF = getdate(self.posting_date)
        company_abbr = frappe.get_cached_value("Company", self.company, "abbr")
        year = dateF.strftime("%y")
        month = dateF.strftime("%m")
        prefix = f"{company_abbr}-{year}{month}-"
        self.name = prefix + getseries(prefix, 4)

    def validate_if_zero_rate_item(self):
        for item in self.get("items"):
            if item.item_code:
                valuation_rate = frappe.get_value(
                    "Item", item.item_code, "valuation_rate"
                )
                if item.rate == 0:
                    frappe.throw(
                        "Sale Rate of <b>Item: {}</b> can't be ZERO".format(
                            item.item_name
                        )
                    )
                if item.rate < valuation_rate:
                    frappe.throw(
                        "Sale Rate({0}) of <b>Item: {1}</b> can't be less than it's Valuation Rate ({2})".format(
                            item.rate, item.item_name, valuation_rate
                        )
                    )
        return

    def validate_back_dated_entry(self):
        posting_date = getdate(self.posting_date)
        if is_last_day_of_month(getdate(posting_date)):
            return

        if not self.amended_from:
            latest_sales_invoice = frappe.get_all(
                "Sales Invoice",
                fields=["MAX(posting_date) as date"],
                filters=[["docstatus", "=", "1"], ["company", "=", self.company]],
            )
            latest_date = latest_sales_invoice[0]["date"]
            if latest_date is not None and posting_date < latest_date:
                frappe.throw(
                    f"Posting Date can't be earlier to the latest Sales Invoice i.e. on {latest_date}. If you still wish to make this entry, it can be done only on the last date of the month. Contact Accounts for help."
                )
        else:
            if self.posting_date != str(
                frappe.get_value("Sales Invoice", self.amended_from, "posting_date")
            ):
                frappe.throw(
                    "You can't have different date than original Sales Invoice."
                )
        return


def is_last_day_of_month(date_obj: date):
    # Get the next day's date
    next_day = date_obj + timedelta(days=1)

    # Check if the next day is in the next month
    return date_obj.month != next_day.month


@frappe.whitelist()
def directly_mark_cancelled(name):
    roles = frappe.get_roles(frappe.session.user)
    if "Accounts User" not in roles:
        frappe.throw(
            "Only Accounts Person is allowed to mark a Draft Sales Invoice directly to Cancelled."
        )
    document = frappe.get_doc("Sales Invoice", name)

    if document.docstatus != 0:
        frappe.throw("Only Draft document is allowed to be set as cancelled.")
    frappe.db.set_value("Sales Invoice", name, "docstatus", 2)
    frappe.db.commit()
