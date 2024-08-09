import frappe
from frappe.utils.data import get_datetime


def validate(self, method=None):
    validate_all_pos_included(self)


def validate_all_pos_included(self):
    rows = frappe.db.sql(
        f"""
                        SELECT name, CONVERT(CONCAT(posting_date, ' ', posting_time), DATETIME)as posting_datetime
                        FROM `tabPOS Invoice`
                        WHERE
                            status in ('Paid','Return') 
                            and docstatus = 1
                            and pos_profile = '{self.pos_profile}'
                            and owner = '{self.user}'
                        HAVING
                            posting_datetime >= '{get_datetime(self.period_start_date).strftime("%Y-%m-%d %H:%M:00")}'
                            and posting_datetime <= '{get_datetime(self.period_end_date).strftime("%Y-%m-%d %H:%M:59")}'
                        """,
        as_dict=1,
    )
    count = len(rows)
    actual_pos_invoices = [r["name"] for r in rows]
    pos_system_invoices = [p.pos_invoice for p in self.pos_transactions]
    exclusive_pos_invoices = get_exclusive_values(
        actual_pos_invoices, pos_system_invoices
    )
    exclusive_pos_invoices_str = ",".join(exclusive_pos_invoices)
    if count != len(self.pos_transactions):
        frappe.throw(
            f"""All the POS Invoices from start time to end time are not included. The reason could be that you are immediately closing the POS after the last POS Invoice."""
            f"""<br><b>Actual Invoices Count</b> : {len(actual_pos_invoices)}"""
            f"""<br><b>POS System Invoices Count</b> : {len(pos_system_invoices)}"""
            f"""<br><b>Exclusive Inoices</b> : {exclusive_pos_invoices_str}"""
        )
    return


def get_exclusive_values(list1, list2):
    # Convert lists to sets
    set1 = set(list1)
    set2 = set(list2)

    # Find values exclusive to each set
    exclusive_to_list1 = set1 - set2
    exclusive_to_list2 = set2 - set1

    # Combine the exclusive values
    exclusive_values = exclusive_to_list1.union(exclusive_to_list2)

    return list(exclusive_values)
