from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
import frappe

class HKMPaymentEntry(PaymentEntry):
    def on_submit(self):
        self.reconcile_bank_transaction_for_entries_from_statement()
        super(HKMPaymentEntry, self).on_submit()
    

    def reconcile_bank_transaction_for_entries_from_statement(self):
        if not self.get("bank_statement_name"):
            return

        bank_transaction = frappe.get_doc("Bank Transaction", self.bank_statement_name)

        # if self.total_debit > bank_transaction.unallocated_amount:
        #     frappe.throw(
        #         frappe._(
        #             f"Total Amount is more than Bank Transaction {bank_transaction.name}'s unallocated amount ({bank_transaction.unallocated_amount})."
        #         )
        #     )

        pe = {
            "payment_document": self.doctype,
            "payment_entry": self.name,
            "allocated_amount": self.paid_amount,
        }
        bank_transaction.append("payment_entries", pe)
        bank_transaction.save(ignore_permissions=True)
        # frappe.db.set_value(
        #     "Journal Entry",
        #     self.name,
        #     {
        #         "clearance_date": bank_transaction.date.strftime("%Y-%m-%d"),
        #         "bank_statement_name": None,
        #     },
        # )
        ## It is important to remove Bank Transaction, when we have used Bank Transaction Name on Submit. Because in case of amendment of the doucment, it will then use same Bank Transaction (Cancelled) to try allocate in reconcillation. This will turn into ERROR.

    
