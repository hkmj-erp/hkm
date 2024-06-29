# Copyright (c) 2022, Tara Technologies and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
import copy
from frappe import _
from frappe.utils import flt, date_diff, getdate, cint, fmt_money, add_days, cint
from erpnext.accounts.utils import get_balance_on
import datetime


def execute(filters):
    return SuspenseReport(filters).get_data()


class SuspenseReport(object):
    def __init__(self, filters):
        self.filters = frappe._dict(filters)
        self.suspense_entries = []
        self.clearance_entries = frappe._dict()
        self.future_clearance_entries = frappe._dict()
        self.show_future_clearance_entries = 0
        self.unlinked_entries = []
        self.suspense_account_balance = frappe._dict()
        self.columns = []
        self.summary = frappe._dict()
        self.message = None
        self.validate_filters()
        self.load_data()
        self.process_data()

    def load_data(self):
        self.load_suspense_entries()
        self.load_clearance_entries()
        self.load_suspense_account_balance()

    def process_data(self):
        self.set_suspense_clearance_entry()
        self.set_report_data()
        self.set_unlinked_entry_to_report_data()
        self.filters_data()
        self.set_report_summary()
        self.set_message()
        self.set_columns()

    def load_suspense_entries(self):
        self.suspense_entries = frappe.db.sql(
            """
			select jv.name, jv.posting_date, jva.credit as suspense_amount, jv.company,
			jv.cheque_no as suspense_jv_bank_ref
			from `tabJournal Entry` jv 
			inner join `tabJournal Entry Account` jva on(jva.parent = jv.name)
			where jv.docstatus = 1
			and jva.credit > 0
			and ifnull(jva.suspense_jv, '') = ''
			-- and jv.name = 'ACC-JV-2022-14286'
			{conditions}
			order by jv.posting_date
			""".format(
                conditions=self.get_conditions()
            ),
            self.filters,
            as_dict=1,
        )

    def load_clearance_entries(self, future_clearance=False):
        conditions = self.get_conditions()

        for d in frappe.db.sql(
            """
			with suspense_clearance as (
				select jv.name as clearing_jv, jv.posting_date, jv.cheque_no, jv.cheque_date, 
				jv.other_reference_number, jv.remark, jv.user_remark,
			    jva.account, jva.suspense_jv, jva.debit as suspense_amount
				from `tabJournal Entry Account` jva
				inner join `tabJournal Entry` jv on (jv.name = jva.parent)
				left join (
					select parent, account, credit from `tabJournal Entry Account` where docstatus = 1 and credit > 0
				)sjv on (sjv.parent = jva.suspense_jv and sjv.account = jva.account)
				where jv.docstatus = 1
				and jva.debit > 0	
				-- and jv.name = 'ACC-JV-2022-14097-1'		
				{conditions}
			),
			suspense_donation as (
				select jva.parent, (jva.debit+jva.credit) as cleared_amount, jva.is_a_donation,
				jva.donor_name, jva.dr_no, jva.receipt_date, jva.online_payment_reference, jva.against_account, 
				jva.devotee, jva.cost_center
				from `tabJournal Entry Account` jva
			    where jva.docstatus = 1
			    and jva.is_a_donation = 1
			)
			select sj.*, sd.*
			from suspense_clearance sj
			left join suspense_donation sd on (sd.parent = sj.clearing_jv)
	
			""".format(
                conditions=self.get_conditions()
            ),
            self.filters,
            as_dict=1,
        ):
            d["entry_amount"] = flt(d.get("cleared_amount")) or flt(
                d.get("suspense_amount")
            )
            d["against_account"] = d.get("against_account") or d.get("account")
            suspense_jv = d.suspense_jv if d.get("suspense_jv") else "Unlinked"
            self.clearance_entries.setdefault(
                suspense_jv, frappe._dict(cleared_amount=0, clearance_entries=[])
            )
            if not d.get("is_a_donation") and d.get("suspense_amount"):
                self.clearance_entries[suspense_jv].cleared_amount += flt(
                    d.suspense_amount
                )
            else:
                self.clearance_entries[suspense_jv].cleared_amount += flt(
                    d.cleared_amount
                )

            self.clearance_entries[suspense_jv].clearance_entries.append(d)

    def load_suspense_account_balance(self):
        self.suspense_account_balance = frappe._dict(
            opening=0,
            closing=0,
        )
        donation_suspense_account = self.filters.get("donation_suspense_account")
        if donation_suspense_account:
            self.suspense_account_balance.opening = get_balance_on(
                account=donation_suspense_account,
                date=add_days(self.filters.from_date, -1),
                company=self.filters.company,
                ignore_account_permission=True,
            )
            self.suspense_account_balance.closing = get_balance_on(
                account=donation_suspense_account,
                date=self.filters.to_date,
                company=self.filters.company,
                ignore_account_permission=True,
            )

    def set_suspense_clearance_entry(self):
        for entry in self.suspense_entries:
            clearance_entry = self.clearance_entries.get(entry.name)
            if clearance_entry:
                entry.update(clearance_entry)
                self.set_suspense_entry_status(entry)

            if not entry.get("status"):
                entry["status"] = "Uncleared"

            entry["uncleared_amount"] = flt(entry.get("suspense_amount")) - flt(
                entry.get("cleared_amount")
            )

    def set_suspense_entry_status(self, entry):
        if flt(entry.get("cleared_amount")) == flt(entry.suspense_amount):
            entry["status"] = "Cleared"
        elif flt(entry.get("cleared_amount")) < 0 or flt(
            entry.get("cleared_amount")
        ) > flt(entry.suspense_amount):
            entry["status"] = "Mismatched"
        elif flt(entry.get("cleared_amount")) and flt(
            entry.get("cleared_amount")
        ) < flt(entry.suspense_amount):
            entry["status"] = "Partially Cleared"

    def filters_data(self):
        if self.filters.status == "Uncleared":
            self.report_data = [
                d
                for d in self.report_data
                if flt(d.uncleared_amount) != 0
                or d.status in ["Unlinked", "Mismatched", "Partially Cleared"]
            ]
        elif not self.filters.status == "All":
            self.report_data = [
                d for d in self.report_data if d.status == self.filters.status
            ]

    def set_report_data(self):
        self.report_data = []
        for entry in self.suspense_entries:
            clearance_entries = entry.get("clearance_entries")
            suspense_entry_row = self.get_suspense_entry_row(entry)
            if not clearance_entries:
                self.report_data.append(suspense_entry_row)
                continue

            rows = []
            for idx, clearing_entry in enumerate(clearance_entries):
                row = suspense_entry_row.copy()
                row.update(self.get_clearing_entry_row(clearing_entry))

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

            self.report_data.extend(rows)

    def set_unlinked_entry_to_report_data(self):
        suspense_jvs = [d.jv_entry for d in self.report_data]
        for suspense_jv, entries in self.clearance_entries.items():
            if suspense_jv in suspense_jvs:
                continue

            clearance_entries = entries.get("clearance_entries") or []
            for entry in clearance_entries:
                row = self.get_clearing_entry_row(entry)
                row["status"] = "Unlinked"
                row["unlinked_amount"] = flt(entry.entry_amount, 2)
                row["cleared_amount"] = flt(entry.entry_amount, 2) * -1
                self.report_data.append(row)

    def get_suspense_entry_row(self, entry):
        return frappe._dict(
            jv_entry=entry.name,
            jv_date=entry.posting_date,
            remarks=entry.user_remark,
            suspense_amount=entry.suspense_amount,
            uncleared_amount=entry.uncleared_amount,
            cleared_amount=entry.cleared_amount,
            company=entry.company,
            suspense_jv_bank_ref=entry.suspense_jv_bank_ref,
            status=entry.status,
        )

    def get_clearing_entry_row(self, entry):
        return frappe._dict(
            clearing_jv=entry.get("clearing_jv"),
            clearing_date=entry.get("posting_date"),
            bank_reference=entry.get("cheque_no"),
            bank_reference_date=entry.get("cheque_date"),
            remark=entry.get("remark"),
            user_remark=entry.get("user_remark"),
            other_reference_number=entry.get("other_reference_number"),
            donor_name=entry.get("donor_name"),
            dr_no=entry.get("dr_no"),
            receipt_date=entry.get("receipt_date"),
            online_reference=entry.get("online_payment_reference"),
            against_account=entry.get("against_account"),
            entry_amount=entry.get("entry_amount"),
            devotee=entry.get("devotee"),
            cost_center=entry.get("cost_center"),
        )

    def get_data(self):
        return self.columns, self.report_data, self.message, None, self.summary

    def get_report_data(self):
        if self.filters.status == "Uncleared" and cint(self.filters.get("sort")):
            self.sort_data()

        return self.report_data

    def get_message(self):
        return self.message

    def get_summary(self):
        return self.summary

    def sort_data(self):
        from operator import itemgetter

        for d in self.report_data:
            d["sorted_value"] = abs(flt(d.get("suspense_amount"))) or abs(
                flt(d.get("cleared_amount"))
            )
        self.report_data = sorted(self.report_data, key=itemgetter("sorted_value"))

    def validate_filters(self):
        if not self.filters.get("from_date") and self.filters.get("to_date"):
            frappe.throw(_("From and To Dates are required."))
        elif date_diff(self.filters.to_date, self.filters.from_date) < 0:
            frappe.throw(_("To Date cannot be before From Date."))

        if not self.filters.get("company"):
            frappe.throw(_("Company is required."))
        else:
            self.filters["donation_suspense_account"] = frappe.get_cached_value(
                "Company", self.filters.company, "donation_suspense_account"
            )
            if not self.filters["donation_suspense_account"]:
                frappe.throw(
                    _(
                        "Please setup <b>Donation Suspense Account</b> under company {0}".format(
                            filters.company
                        )
                    )
                )

    def get_report_data_totals(self):
        totals = frappe._dict(
            suspense_amount=0,
            cleared_amount=0,
            uncleared_amount=0,
            mismatched_amount=0,
            unlinked_amount=0,
        )
        for d in self.report_data:
            totals["suspense_amount"] -= flt(d.get("suspense_amount"))
            if d.status == "Unlinked":
                totals["unlinked_amount"] += flt(d.get("unlinked_amount"))
            elif d.status in ["Mismatched", "Partially Cleared"]:
                totals["mismatched_amount"] += flt(d.get("entry_amount"))
            elif d.status == "Cleared":
                totals["cleared_amount"] += flt(d.get("cleared_amount"))
            elif d.status == "Uncleared":
                totals["uncleared_amount"] += flt(d.get("uncleared_amount"))

        totals["total_cleared_amount"] = (
            flt(totals.cleared_amount)
            + flt(totals.unlinked_amount)
            + flt(totals.mismatched_amount)
        )
        totals["net_suspense_balance"] = (
            totals.suspense_amount + totals.total_cleared_amount
        )
        totals["total_suspense_balance"] = flt(
            self.suspense_account_balance.opening
        ) + flt(totals.net_suspense_balance)
        return totals

    def set_report_summary(self):
        totals = self.get_report_data_totals()
        self.summary = [
            dict(
                label="Total Suspense",
                value=abs(flt(totals.suspense_amount)),
                indicator="Blue",
                datatype="Currency",
            )
        ]

        if self.filters.status != "All":
            amount = 0
            if self.filters.status == "Uncleared":
                amount = flt(totals.uncleared_amount, 2)
            elif self.filters.status == "Unlinked":
                amount = flt(totals.unlinked_amount, 2)
            elif self.filters.status in ["Mismatched", "Partially Cleared"]:
                amount = flt(totals.mismatched_amount, 2)
            elif self.filters.status == "Cleared":
                amount = flt(totals.cleared_amount, 2)

            if self.filters.status == "Uncleared":
                self.summary.extend(
                    [
                        dict(
                            label="Unlinked Cleared",
                            value=flt(totals.unlinked_amount, 2),
                            indicator="Blue",
                            datatype="Currency",
                        ),
                        dict(
                            label="Mismatched/Partially Cleared",
                            value=flt(totals.mismatched_amount, 2),
                            indicator="Blue",
                            datatype="Currency",
                        ),
                        dict(
                            label="Uncleared",
                            value=abs(flt(totals.net_suspense_balance, 2)),
                            indicator="Blue",
                            datatype="Currency",
                        ),
                    ]
                )
            else:
                self.summary.extend(
                    [
                        dict(
                            label=self.filters.status,
                            value=amount,
                            indicator="Blue",
                            datatype="Currency",
                        )
                    ]
                )
        else:
            self.summary.extend(
                [
                    {"type": "separator", "value": "-"},
                    dict(
                        label="Cleared",
                        value=totals.cleared_amount,
                        indicator="Green",
                        datatype="Currency",
                    ),
                    {"type": "separator", "value": "="},
                    dict(
                        label="Uncleared",
                        value=abs(totals.uncleared_amount),
                        indicator="Orange",
                        datatype="Currency",
                    ),
                    dict(
                        label="Mismatched/Partially Cleared",
                        value=abs(totals.mismatched_amount),
                        indicator="Red",
                        datatype="Currency",
                    ),
                ]
            )

    def set_message(self):
        totals = self.get_report_data_totals()
        self.message = """
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Opening Balance : </div>
				</div>
				<div class="col-xs-2 column-break" >
					<div class="text-right">{op_balance}</div>
				</div>								
			</div>		
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Suspense Amount : </div>
				</div>
				<div class="col-xs-1 column-break" >
					<div class="text-right">{suspense_amount}</div>
				</div>	
				<div class="col-xs-1 column-break" ></div>

			</div>		
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Cleared Amount : </div>
				</div>
				<div class="col-xs-1 column-break" >
					<div class="text-right">{cleared_amount}</div>
				</div>	
				<div class="col-xs-1 column-break" ></div>				
			</div>					
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Unlinked Cleared Amount : </div>
				</div>
				<div class="col-xs-1 column-break" >
					<div class="text-right">{unlinked_amount}</div>
				</div>	
				<div class="col-xs-1 column-break" ></div>								
			</div>	
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Mismatched/Partially Cleared Amount : </div>
					
				</div>
				<div class="col-xs-1 column-break" >
					<div class="text-right">{mismatched_amount}</div>
				</div>	
				<div class="col-xs-1 column-break" ></div>												
			</div>				
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Net Amount : </div>
				</div>
				<div class="col-xs-1 column-break border-top" >
					<div class="text-right">{net_suspense_balance}</div>
				</div>	
				<div class="col-xs-1 column-break border-top" >
					<div class="text-right">{total_suspense_balance}</div>
				</div>																
			</div>																		
			<div class="row section-break bold">
				<div class="col-xs-6 column-break" ></div>
				<div class="col-xs-4 column-break" >
					<div class="text-right">Closing Balance : </div>
				</div>
				<div class="col-xs-2 column-break border-top" >
					<div class="text-right">{cl_balance}</div>
				</div>								
			</div>
		""".format(
            op_balance=self.suspense_account_balance.opening,
            suspense_amount=flt(totals.suspense_amount, 2),
            cleared_amount=totals.cleared_amount,
            unlinked_amount=totals.unlinked_amount,
            mismatched_amount=totals.mismatched_amount,
            total_cleared_amount=flt(totals.total_cleared_amount, 2),
            net_suspense_balance=flt(totals.net_suspense_balance, 2),
            total_suspense_balance=flt(totals.total_suspense_balance, 2),
            cl_balance=self.suspense_account_balance.closing,
        )

    def set_columns(self):
        self.columns = []
        if self.filters.status != "Unlinked":
            self.columns.extend(
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
        if not self.filters.get("group_jv"):
            self.columns.extend(
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

    def get_conditions(self):
        conditions = ""
        if self.filters.get("company"):
            conditions += " and jv.company = %(company)s"
        if self.filters.get("from_date"):
            conditions += " and jv.posting_date >= %(from_date)s"
        if self.filters.get("to_date"):
            conditions += " and jv.posting_date <= %(to_date)s"
        if self.filters.get("donation_suspense_account"):
            conditions += " and jva.account = %(donation_suspense_account)s"

        return conditions
