# Copyright (c) 2024, Narahari Dasa and contributors
# For license information, please see license.txt

from erpnext.accounts.report.bank_reconciliation_statement.bank_reconciliation_statement import (
    get_amounts_not_reflected_in_system,
    get_entries,
)
from erpnext.accounts.utils import get_balance_on
import frappe
from frappe import _
from frappe.utils.data import flt


def execute(filters=None):
    columns, data = [], []
    if not filters:
        filters = {}

    columns = get_columns()
    account_currency = frappe.get_cached_value(
        "Account", filters.account, "account_currency"
    )
    balance_as_per_system = get_balance_on(filters["account"], filters["report_date"])
    reco_entries = get_entries(filters)

    total_debit, total_credit = 0, 0
    for d in reco_entries:
        total_debit += flt(d.debit)
        total_credit += flt(d.credit)

    amounts_not_reflected_in_system = get_amounts_not_reflected_in_system(filters)

    bank_tx_debit, bank_tx_credit = get_amounts_from_bank_transactions(filters)

    bank_bal = (
        flt(balance_as_per_system)
        # - flt(total_debit)
        # + flt(total_credit)
        + amounts_not_reflected_in_system
        + flt(bank_tx_debit)
        - flt(bank_tx_credit)
    )

    data += [
        get_balance_row(
            _("Bank Statement balance as per General Ledger"),
            balance_as_per_system,
            account_currency,
        ),
        {},
        {
            "subject": _("Outstanding Cheques and Deposits to clear"),
            "debit": total_debit,
            "credit": total_credit,
            "account_currency": account_currency,
        },
        get_balance_row(
            _("Cheques and Deposits incorrectly cleared"),
            amounts_not_reflected_in_system,
            account_currency,
        ),
        {},
        {
            "subject": _("Outstanding Bank Transactions to clear"),
            "debit": bank_tx_debit,
            "credit": bank_tx_credit,
            "account_currency": account_currency,
        },
        {},
        get_balance_row(
            _("Calculated Bank Statement balance"), bank_bal, account_currency
        ),
    ]

    return columns, data


def get_columns():
    return [
        {
            "fieldname": "subject",
            "label": _("Subject"),
            "fieldtype": "Data",
            "width": 400,
        },
        {
            "fieldname": "debit",
            "label": _("Debit"),
            "fieldtype": "Currency",
            "options": "account_currency",
            "width": 120,
        },
        {
            "fieldname": "credit",
            "label": _("Credit"),
            "fieldtype": "Currency",
            "options": "account_currency",
            "width": 120,
        },
    ]


def get_balance_row(label, amount, account_currency):
    if amount > 0:
        return {
            "subject": label,
            "debit": amount,
            "credit": 0,
            "account_currency": account_currency,
        }
    else:
        return {
            "subject": label,
            "debit": 0,
            "credit": abs(amount),
            "account_currency": account_currency,
        }


def get_amounts_from_bank_transactions(filters):
    bank_account = frappe.get_value(
        "Bank Account", {"account": filters.account}, "name"
    )
    s = frappe.db.sql(
        f"""
			SELECT 
                SUM(IF(deposit > 0, unallocated_amount,0)) as debit,
                SUM(IF(withdrawal > 0, unallocated_amount,0)) as credit
			FROM `tabBank Transaction`
			WHERE 
            	status = 'Unreconciled' 
                and docstatus = 1 
                and bank_account = '{bank_account}' 
                and `date` <= '{filters.get("report_date")}'
					"""
    )
    if s:
        return s[0]
    else:
        return [0, 0]
