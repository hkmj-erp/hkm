# Copyright (c) 2021, Tara Technologies
# For license information, please see license.txt

from __future__ import unicode_literals
from erpnext.accounts.doctype import payment_entry
import frappe
from frappe import _, throw
from frappe.utils import flt
from erpnext.accounts.doctype.journal_entry.journal_entry import JournalEntry
from frappe.utils.data import getdate
from frappe.model.naming import getseries


class HKMJournalEntry(JournalEntry):
    def autoname(self):
        dateF = getdate(self.posting_date)
        company_abbr = frappe.get_cached_value("Company", self.company, "abbr")
        year = dateF.strftime("%y")
        month = dateF.strftime("%m")
        prefix = f"{company_abbr}-JV-{year}{month}-"
        self.name = prefix + getseries(prefix, 5)

    def on_submit(self):
        self.validate_gst_entry()
        self.reconcile_bank_transaction_for_entries_from_statement()
        super(HKMJournalEntry, self).on_submit()

    def on_cancel(self):
        super(HKMJournalEntry, self).on_cancel()

    def validate_gst_entry(self):
        from hkm.erpnext___custom.extend.accounts_controller import validate_gst_entry

        validate_gst_entry(self)

    def reconcile_bank_transaction_for_entries_from_statement(self):
        if not self.get("bank_statement_name"):
            return

        bank_transaction = frappe.get_doc("Bank Transaction", self.bank_statement_name)

        if self.total_debit > bank_transaction.unallocated_amount:
            frappe.throw(
                frappe._(
                    f"Total Amount is more than Bank Transaction {bank_transaction.name}'s unallocated amount ({bank_transaction.unallocated_amount})."
                )
            )

        pe = {
            "payment_document": self.doctype,
            "payment_entry": self.name,
            "allocated_amount": self.total_debit,
        }
        bank_transaction.append("payment_entries", pe)
        bank_transaction.save(ignore_permissions=True)
        frappe.db.set_value(
            "Journal Entry",
            self.name,
            {
                "clearance_date": bank_transaction.date.strftime("%Y-%m-%d"),
                "bank_statement_name": None,
            },
        )
        ## It is important to remove Bank Transaction, when we have used Bank Transaction Name on Submit. Because in case of amendment of the doucment, it will then use same Bank Transaction (Cancelled) to try allocate in reconcillation. This will turn into ERROR.


## Same above can also be achieved by writing above lines on cancellation hook.


def update_suspense_jv_cleared_amount(suspense_jv=None):
    conditions = ""
    if suspense_jv:
        conditions = " and jv.name='%s'" % suspense_jv

    frappe.db.sql(
        """
		update `tabJournal Entry` jv 
		inner join `tabJournal Entry Account` jva on(jva.parent = jv.name)
		inner join `tabCompany` comp on (comp.name = jv.company)
		left join (
			select cl.suspense_jv, cl.account, sum((cl.debit+(cl.credit*-1))) as cleared_amount
			from `tabJournal Entry Account` cl
			where cl.docstatus = 1
			group by cl.suspense_jv, cl.account
		) cl on (cl.suspense_jv = jv.name and cl.account = jva.account)
		set jv.cleared_amount = ifnull(cl.cleared_amount, 0),
			jv.uncleared_amount = jva.credit - ifnull(cl.cleared_amount, 0)
		where jv.docstatus = 1
		and jva.account = comp.donation_suspense_account
		and ifnull(jva.suspense_jv, '') = ''
		{0}""".format(
            conditions
        )
    )


@frappe.whitelist()
def get_journal_entry_from_statement(statement):
    bank_transaction = frappe.get_doc("Bank Transaction", statement)
    company_account = frappe.get_value(
        "Bank Account", bank_transaction.bank_account, "account"
    )

    accounts = []
    COST_CENTER = frappe.db.get_value(
        "Company", bank_transaction.company, "cost_center"
    )
    accounts.append(
        {
            # "account": "",
            "credit_in_account_currency": bank_transaction.deposit,
            "debit_in_account_currency": bank_transaction.withdrawal,
            "cost_center": COST_CENTER,
        }
    )

    accounts.append(
        {
            "account": company_account,
            "bank_account": bank_transaction.bank_account,
            "credit_in_account_currency": bank_transaction.withdrawal,
            "debit_in_account_currency": bank_transaction.deposit,
            "cost_center": COST_CENTER,
        }
    )

    company = frappe.get_value("Account", company_account, "company")

    journal_entry_dict = {
        "voucher_type": "Bank Entry",
        "company": company,
        "bank_statement_name": bank_transaction.name,
        "posting_date": bank_transaction.date,
        "cheque_date": bank_transaction.date,
        "cheque_no": bank_transaction.description,
    }
    journal_entry = frappe.new_doc("Journal Entry")
    journal_entry.update(journal_entry_dict)
    journal_entry.set("accounts", accounts)
    return journal_entry


@frappe.whitelist()
def unallocate_bank_transaction(je):
    je_doc = frappe.get_doc("Journal Entry", je)
    if not je_doc.bank_statement_name:
        return

    tx = frappe.db.get_list(
        "Bank Transaction",
        filters={"payment_document": "Journal Entry", "payment_entry": je},
    )
    if len(tx) != 1:
        frappe.throw(
            "There is not a SINGLE Bank Transaction Entry. Either 0 or more than 1. Contact Administrator."
        )
    tx = tx[0]
    tx_doc = frappe.get_doc("Bank Transaction", tx)
    row = next(r for r in tx_doc.payment_entries if r.payment_entry == je)
    tx_doc.remove(row)
    tx_doc.save()

    je_doc.bank_statement_name = None
    je_doc.clearance_date = None

    frappe.db.set_value(
        "Journal Entry", je, {"bank_statement_name": None, "clearance_date": None}
    )
    frappe.db.commit()
