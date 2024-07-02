# from erpnext.accounts.doctype.payment_entry.payment_entry import PaymentEntry
# import frappe


# class HKMPaymentEntry(PaymentEntry):

#     def on_submit(self):
#         frappe.throw("ERROR")
#         super(HKMPaymentEntry, self).on_submit()
#         self.reconcile_bank_transaction_for_entries_from_statement()

#     def reconcile_bank_transaction_for_entries_from_statement(self):
#         frappe.errprint(self.get("bank_statement_name"))
#         frappe.errprint("Hare Krishna")
#         if not self.get("bank_statement_name"):
#             return

#         bank_transaction = frappe.get_doc("Bank Transaction", self.bank_statement_name)

#         if self.paid_amount > bank_transaction.unallocated_amount:
#             frappe.throw(
#                 frappe._(
#                     f"Total Paid Amount can not be more than Bank Transaction {bank_transaction.name}'s unallocated amount ({bank_transaction.unallocated_amount})."
#                 )
#             )

#         pe = {
#             "payment_document": self.doctype,
#             "payment_entry": self.name,
#             "allocated_amount": self.paid_amount,
#         }
#         frappe.errprint(pe)
#         bank_transaction.append("payment_entries", pe)
#         bank_transaction.save(ignore_permissions=True)
#         frappe.db.set_value(
#             "Payment Entry",
#             self.name,
#             {
#                 "clearance_date": bank_transaction.date.strftime("%Y-%m-%d"),
#                 "bank_statement_name": None,
#             },
#             update_modified=False,
#         )
#         frappe.db.commit()


# @frappe.whitelist()
# def get_payment_entry_from_statement(statement):
#     bank_transaction = frappe.get_doc("Bank Transaction", statement)
#     company_account = frappe.get_value(
#         "Bank Account", bank_transaction.bank_account, "account"
#     )
#     account_currency = frappe.get_value("Account", company_account, "account_currency")

#     payment_entry_dict = frappe._dict(
#         company=bank_transaction.company,
#         payment_type="Receive" if bank_transaction.deposit > 0 else "Pay",
#         party_type="Supplier",
#         paid_from=company_account,
#         paid_amount=bank_transaction.withdrawal,
#         received_amount=bank_transaction.withdrawal,
#         paid_from_account_currency=account_currency,
#         posting_date=bank_transaction.date,
#         bank_statement_name=bank_transaction.name,
#         reference_no=bank_transaction.description,
#         reference_date=bank_transaction.date,
#     )

#     payment_entry = frappe.new_doc("Payment Entry")
#     payment_entry.update(payment_entry_dict)
#     return payment_entry
