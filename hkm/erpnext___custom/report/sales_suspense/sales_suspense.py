# Copyright (c) 2013, Narahari Das and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import copy
from frappe import _
from frappe.utils import flt, date_diff, getdate, cint, fmt_money


def execute(filters=None):
    if not filters:
        return [], []

    if cint(filters.get("show_new")):
        return new_suspense_report(filters)
    else:
        return old_suspense_report(filters)


def new_suspense_report(filters):
    from hkm.erpnext___custom.report.sales_suspense.sales_suspense_new import (
        SuspenseReport,
    )

    report = SuspenseReport(filters)
    data = report.get_report_data()
    columns = get_columns(filters)
    if filters.get("status") == "All":
        message = report.get_message()
        return columns, data, message
    else:
        summary = report.get_summary()
        return columns, data, None, None, summary


def old_suspense_report(filters):
    validate_filters(filters)
    columns = get_columns(filters)
    data, message, summary = get_data(filters)

    return columns, data, message, None, summary


def get_data(filters):
    data = []
    summary = []
    message = ""
    if filters.status == "Unlinked":
        data = get_unlinked_entries(filters)
        summary = get_report_summary(data, filters) or []
        return data, message, summary

    suspnese_entries = get_suspnese_entries(filters)
    if suspnese_entries:
        clearing_entries = get_clearing_entries(suspnese_entries)
        data = get_process_data(suspnese_entries, clearing_entries, filters)
        data = get_filter_data(data, filters)

    summary = get_report_summary(data, filters) or []

    if filters.status in ["All"]:
        message = get_message(data)

    return data, message, summary


def get_process_data(suspnese_entries, clearing_entries, filters):
    data = []
    for entry in suspnese_entries:
        suspense_clearing_entries = clearing_entries.get(entry.name, [])
        suspense_amount = flt(entry.suspense_amount)
        total_cleared_amount = 0
        suspense_entry_row = get_suspense_entry_row(entry)
        rows = []
        if suspense_clearing_entries:
            total_cleared_amount = flt(
                sum([flt(k[1]) for k, entries in suspense_clearing_entries.items()])
            )
            uncleared_amount = flt(suspense_amount) - flt(total_cleared_amount)
            suspense_entry_row.update(
                frappe._dict(
                    cleared_amount=total_cleared_amount,
                    uncleared_amount=uncleared_amount,
                    status=get_status(suspense_amount, total_cleared_amount),
                )
            )
            if cint(filters.get("group_jv")):
                data.append(suspense_entry_row)
                continue

            cl_entries = []
            for cl_entry in suspense_clearing_entries.values():
                cl_entries.extend(cl_entry)

            for idx, clearing_entry in enumerate(cl_entries):
                row = suspense_entry_row.copy()
                row.update(get_clearing_entry_row(clearing_entry))

                # clear amount to avoid incorrect totals due to multiple clearing entries
                if idx != 0:
                    row.update(
                        frappe._dict(
                            suspense_amount=None,
                            cleared_amount=None,
                            uncleared_amount=None,
                        )
                    )

                rows.append(row)

        else:
            suspense_entry_row.update(
                frappe._dict(
                    status=get_status(suspense_amount, total_cleared_amount),
                )
            )
            rows.append(suspense_entry_row)

        data.extend(rows)

    return data


def get_status(suspense_amount, cleared_amount=0):
    if cleared_amount == 0:
        return "Uncleared"
    elif cleared_amount < 0 or cleared_amount > suspense_amount:
        return "Mismatched"
    elif cleared_amount < suspense_amount:
        return "Partially Cleared"
    else:
        return "Cleared"


def get_filter_data(processed_data, filters):
    data = []
    for row in processed_data:
        if filters.status == "All":
            data.append(row)
        elif filters.status == "Cleared" and row.status in [
            "Cleared",
            "Partially Cleared",
        ]:
            data.append(row)
        elif filters.status == "Uncleared" and row.status in [
            "Uncleared",
            "Partially Cleared",
        ]:
            data.append(row)
        elif filters.status == row.status:
            data.append(row)

    return data


def get_suspense_entry_row(entry):
    return frappe._dict(
        jv_entry=entry.name,
        jv_date=entry.posting_date,
        remarks=entry.user_remark,
        suspense_amount=entry.suspense_amount,
        uncleared_amount=entry.suspense_amount,
        cleared_amount=0,
        company=entry.company,
        suspense_jv_bank_ref=entry.cheque_no,
    )


def get_clearing_entry_row(entry):
    return frappe._dict(
        clearing_jv=entry.get("clearing_jv"),
        clearing_date=entry.get("clearing_date"),
        bank_reference=entry.get("cheque_no"),
        bank_reference_date=entry.get("cheque_date"),
        donor_name=entry.get("donor_name"),
        dr_no=entry.get("dr_no"),
        receipt_date=entry.get("receipt_date"),
        online_reference=entry.get("online_payment_reference"),
        remark=entry.get("remark"),
        user_remark=entry.get("user_remark"),
        other_reference_number=entry.get("other_reference_number"),
        against_account=entry.get("against_account"),
        entry_amount=entry.get("entry_amount"),
        devotee=entry.get("devotee"),
        cost_center=entry.get("cost_center"),
    )


def get_suspnese_entries(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """
		select jv.name, jv.posting_date,jv.user_remark, jva.credit as suspense_amount, jv.company,
		jv.cheque_no, jv.cheque_date
		from `tabJournal Entry` jv 
		inner join `tabJournal Entry Account` jva on(jva.parent = jv.name)
		inner join `tabCompany` comp on (comp.name = jv.company)
		where jv.docstatus = 1
		and jva.account = comp.donation_suspense_account
		and jva.credit > 0
		and ifnull(jva.suspense_jv, '') = ''
		{conditions}
		order by jv.posting_date
		""".format(
            conditions=conditions
        ),
        filters,
        as_dict=1,
    )


def get_clearing_entries(suspnese_entries):
    clearing_entries = frappe._dict()
    for d in frappe.db.sql(
        """
			select jv.name as clearing_jv, jv.posting_date as clearing_date, jv.cheque_no, jv.cheque_date,
			sadj.name as sadj_name, (sadj.debit+(sadj.credit*-1)) as cleared_amount, 
			jva.donor_name, jva.dr_no, jva.receipt_date, jva.online_payment_reference, jva.against_account, 
			jva.entry_amount, jva.devotee, jva.cost_center, 
			jv.other_reference_number, jv.remark, jv.user_remark,
			sadj.suspense_jv
			from `tabJournal Entry` jv 
			inner join `tabJournal Entry Account` sadj on (sadj.parent = jv.name)
			inner join `tabCompany` comp on (comp.name = jv.company)
			inner join (
			select jva.parent, jva.donor_name, jva.dr_no, jva.receipt_date, jva.online_payment_reference,
			(jva.credit + (jva.debit*-1)) as entry_amount,
			jva.account, accn.account_name as against_account, jva.devotee, jva.cost_center
			from `tabJournal Entry Account` as jva
			inner join `tabAccount` as accn on (accn.name = jva.account)
			where (jva.credit + jva.debit) > 0
			) jva on (jva.parent = jv.name)
			where jv.docstatus = 1
			and sadj.account = comp.donation_suspense_account
			and jva.account != sadj.account
			and sadj.suspense_jv in (%s)"""
        % ", ".join(["%s"] * len(suspnese_entries)),
        tuple([jv.name for jv in suspnese_entries]),
        as_dict=1,
    ):
        clearing_entries.setdefault(d.suspense_jv, {}).setdefault(
            (d.sadj_name, d.cleared_amount), []
        ).append(d)
    return clearing_entries


def get_unlinked_entries(filters):
    conditions = get_conditions(filters)
    return frappe.db.sql(
        """
			select jv.name as clearing_jv, jv.posting_date as clearing_date, 
			jv.cheque_no as bank_reference, jv.cheque_date as bank_reference_date,
			jva.credit cleared_amount, jva.credit as entry_amount, jva.account as against_account,
			jva.donor_name, jva.dr_no, jva.receipt_date, jva.online_payment_reference, jva.devotee, jva.cost_center
			from `tabJournal Entry` jv 
			inner join `tabJournal Entry Account` sadj on (sadj.parent = jv.name)
			inner join `tabJournal Entry Account` jva on (jva.parent = jv.name)
			inner join `tabCompany` comp on (comp.name = jv.company)
			where jv.docstatus = 1
			and jva.credit > 0
			and sadj.debit > 0
			and sadj.account = comp.donation_suspense_account
			and ifnull(sadj.suspense_jv,'') = '' 
			{conditions}
			order by jv.posting_date
		""".format(
            conditions=conditions
        ),
        filters,
        as_dict=1,
    )


def get_conditions(filters):
    conditions = ""
    if filters.get("company"):
        conditions += " and jv.company = %(company)s"
    if filters.get("from_date"):
        conditions += " and jv.posting_date >= %(from_date)s"
    if filters.get("to_date"):
        conditions += " and jv.posting_date <= %(to_date)s"
    if filters.get("jv_entry"):
        conditions += " and jv.name = %(jv_entry)s"
    return conditions


def validate_filters(filters):
    from_date, to_date = filters.get("from_date"), filters.get("to_date")

    if not from_date and to_date:
        frappe.throw(_("From and To Dates are required."))
    elif date_diff(to_date, from_date) < 0:
        frappe.throw(_("To Date cannot be before From Date."))

    if filters.get("company") and not frappe.get_cached_value(
        "Company", filters.company, "donation_suspense_account"
    ):
        frappe.throw(
            _(
                "Please setup <b>Donation Suspense Account</b> under company {0}".format(
                    filters.company
                )
            )
        )


def get_message(data):
    mismatch_cleared_amount = sum(
        [
            flt(d.get("cleared_amount"))
            for d in data
            if d.status == "Mismatched" and d.get("cleared_amount")
        ]
    )
    mismatch_uncleared_amount = abs(
        sum(
            [
                flt(d.get("uncleared_amount"))
                for d in data
                if flt(d.get("uncleared_amount")) < 0 and d.get("uncleared_amount")
            ]
        )
    )
    return """<span class='strong text-danger'>
			Both Cleared and Uncleared Amount are exclusive of mismatched suspense entries.
			<br> Mismatched cleared amount : {0} and uncleared amount : {1} (excess/deficit)
			</span>
			""".format(
        fmt_money(mismatch_cleared_amount), fmt_money(mismatch_uncleared_amount)
    )


def get_report_summary(data, filters):
    summary = frappe._dict(
        total_suspense=0,
        total_cleared=0,
        total_uncleared=0,
        mismatched=0,
    )
    for d in data:
        summary["total_suspense"] += flt(d.suspense_amount, 2)
        if d.status != "Mismatched" and d.cleared_amount:
            summary["total_cleared"] += flt(d.cleared_amount, 2)

        if flt(d.get("uncleared_amount")) > 0:
            summary["total_uncleared"] += flt(d.uncleared_amount, 2)
        elif flt(d.get("uncleared_amount")) < 0:
            summary["mismatched"] += flt(d.uncleared_amount, 2)

    return [
        dict(
            label="Total Suspense",
            value=summary.total_suspense,
            indicator="Blue",
            datatype="Currency",
        ),
        {"type": "separator", "value": "-"},
        dict(
            label="Cleared",
            value=summary.total_cleared,
            indicator="Green",
            datatype="Currency",
        ),
        {"type": "separator", "value": "="},
        dict(
            label="Uncleared",
            value=abs(summary.total_uncleared),
            indicator="Orange",
            datatype="Currency",
        ),
        dict(
            label="Mismatched",
            value=abs(summary.mismatched),
            indicator="Red",
            datatype="Currency",
        ),
    ]


def get_columns(filters):
    columns = []
    if filters.status != "Unlinked":
        columns.extend(
            [
                {
                    "label": _("Suspense JV"),
                    "fieldname": "jv_entry",
                    "fieldtype": "Link",
                    "options": "Journal Entry",
                    "width": 180,
                },
                {
                    "label": _("Suspense JV Date"),
                    "fieldname": "jv_date",
                    "fieldtype": "Date",
                    "width": 120,
                },
                {
                    "label": _("Suspense JV Bank Ref."),
                    "fieldname": "suspense_jv_bank_ref",
                    "fieldtype": "Data",
                    "width": 120,
                },
                {
                    "label": _("Suspense Amount"),
                    "fieldname": "suspense_amount",
                    "fieldtype": "Currency",
                    "width": 150,
                },
                {
                    "label": _("Remarks"),
                    "fieldname": "remarks",
                    "fieldtype": "Data",
                    "width": 150,
                },
                {
                    "label": _("Cleared"),
                    "fieldname": "cleared_amount",
                    "fieldtype": "Currency",
                    "width": 130,
                },
                {
                    "label": _("Uncleared"),
                    "fieldname": "uncleared_amount",
                    "fieldtype": "Currency",
                    "width": 130,
                },
                {
                    "label": _("Status"),
                    "fieldname": "status",
                    "fieldtype": "Data",
                    "width": 150,
                },
            ]
        )
    if not filters.get("group_jv"):
        columns.extend(
            [
                {
                    "label": _("Clearing JV"),
                    "fieldname": "clearing_jv",
                    "fieldtype": "Link",
                    "options": "Journal Entry",
                    "width": 180,
                },
                {
                    "label": _("Entry Amount"),
                    "fieldname": "entry_amount",
                    "fieldtype": "Currency",
                    "width": 130,
                },
                {
                    "label": _("Against"),
                    "fieldname": "against_account",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Clearing Date"),
                    "fieldname": "clearing_date",
                    "fieldtype": "Date",
                    "width": 130,
                },
                {
                    "label": _("Bank Reference"),
                    "fieldname": "bank_reference",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Bank Reference Date"),
                    "fieldname": "bank_reference_date",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Donor Name"),
                    "fieldname": "donor_name",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("DR No."),
                    "fieldname": "dr_no",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Receipt Date"),
                    "fieldname": "receipt_date",
                    "fieldtype": "Date",
                    "width": 130,
                },
                {
                    "label": _("Online Reference"),
                    "fieldname": "online_reference",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Devotee"),
                    "fieldname": "devotee",
                    "fieldtype": "Link",
                    "options": "Devotee",
                    "width": 130,
                },
                {
                    "label": _("Remark"),
                    "fieldname": "remark",
                    "fieldtype": "Small Text",
                    "width": 300,
                },
                {
                    "label": _("User Remark"),
                    "fieldname": "user_remark",
                    "fieldtype": "Small Text",
                    "width": 300,
                },
                {
                    "label": _("Other Reference Number"),
                    "fieldname": "other_reference_number",
                    "fieldtype": "Small Text",
                    "width": 200,
                },
                {
                    "label": _("Cost Center"),
                    "fieldname": "cost_center",
                    "fieldtype": "Link",
                    "options": "Cost Center",
                    "width": 150,
                },
                {
                    "label": _("Company"),
                    "fieldname": "company",
                    "fieldtype": "Link",
                    "options": "Company",
                    "width": 130,
                },
            ]
        )

    return columns


def zzzzget_columns(filters):
    columns = []
    if filters.status != "Unlinked":
        columns.extend(
            [
                {
                    "label": _("Suspense JV"),
                    "fieldname": "jv_entry",
                    "fieldtype": "Link",
                    "options": "Journal Entry",
                    "width": 180,
                },
                {
                    "label": _("Suspense JV Date"),
                    "fieldname": "jv_date",
                    "fieldtype": "Date",
                    "width": 120,
                },
                {
                    "label": _("Suspense JV Bank Ref."),
                    "fieldname": "suspense_jv_bank_ref",
                    "fieldtype": "Data",
                    "width": 120,
                },
                {
                    "label": _("Suspense Amount"),
                    "fieldname": "suspense_amount",
                    "fieldtype": "Currency",
                    "width": 150,
                },
                {
                    "label": _("Cleared"),
                    "fieldname": "cleared_amount",
                    "fieldtype": "Float",
                    "width": 130,
                },
                {
                    "label": _("Uncleared"),
                    "fieldname": "uncleared_amount",
                    "fieldtype": "Float",
                    "width": 130,
                },
                {
                    "label": _("Status"),
                    "fieldname": "status",
                    "fieldtype": "Data",
                    "width": 150,
                },
            ]
        )
    if not filters.get("group_jv"):
        columns.extend(
            [
                {
                    "label": _("Entry Amount"),
                    "fieldname": "entry_amount",
                    "fieldtype": "Currency",
                    "width": 130,
                },
                {
                    "label": _("Against"),
                    "fieldname": "against_account",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Clearing JV"),
                    "fieldname": "clearing_jv",
                    "fieldtype": "Link",
                    "options": "Journal Entry",
                    "width": 180,
                },
                {
                    "label": _("Clearing Date"),
                    "fieldname": "clearing_date",
                    "fieldtype": "Date",
                    "width": 130,
                },
                {
                    "label": _("Bank Reference"),
                    "fieldname": "bank_reference",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Bank Reference Date"),
                    "fieldname": "bank_reference_date",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Donor Name"),
                    "fieldname": "donor_name",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("DR No."),
                    "fieldname": "dr_no",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Receipt Date"),
                    "fieldname": "receipt_date",
                    "fieldtype": "Date",
                    "width": 130,
                },
                {
                    "label": _("Online Reference"),
                    "fieldname": "online_reference",
                    "fieldtype": "Data",
                    "width": 130,
                },
                {
                    "label": _("Devotee"),
                    "fieldname": "devotee",
                    "fieldtype": "Link",
                    "options": "Devotee",
                    "width": 130,
                },
                {
                    "label": _("Cost Center"),
                    "fieldname": "cost_center",
                    "fieldtype": "Link",
                    "options": "Cost Center",
                    "width": 150,
                },
                {
                    "label": _("Company"),
                    "fieldname": "company",
                    "fieldtype": "Link",
                    "options": "Company",
                    "width": 130,
                },
            ]
        )
    return columns
