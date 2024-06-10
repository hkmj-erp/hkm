# # Copyright (c) 2023, Narahari Dasa and contributors
# # For license information, please see license.txt

from erpnext.controllers.taxes_and_totals import (
    get_itemised_tax,
    get_itemised_tax_breakup_data,
    get_itemised_taxable_amount,
)
import frappe, json
from frappe import _

GST_SLABS = [0.0, 3.0, 5.0, 12.0, 18.0, 28.0]
GST_TYPES = ["CGST", "SGST", "IGST"]


def slab_types():
    data = []
    for gt in GST_TYPES:
        for sl in GST_SLABS:
            if "IGST" in gt:
                data.append(gt + "-" + str(sl))
            else:
                data.append(gt + "-" + str(sl / 2))
    return data


def execute(filters=None):
    if not filters:
        filters = {}
    filters.update(
        {
            "from_date": filters.get("date_range") and filters.get("date_range")[0],
            "to_date": filters.get("date_range") and filters.get("date_range")[1],
        }
    )

    columns = get_columns(filters)

    invoices = get_invoices(filters)

    data = []
    for inv in invoices:
        for slab in GST_SLABS:
            row_include = False
            row = get_blank_row(inv)
            total_tax = 0
            hsns = []
            for gt in GST_TYPES:
                if gt == "IGST":
                    head = gt + "-" + str(slab)
                else:
                    head = gt + "-" + str(slab / 2)
                if head in invoices[inv]["taxes"]:
                    row_include = True
                    row["posting_date"] = invoices[inv]["details"]["posting_date"]
                    row["customer_name"] = invoices[inv]["details"]["customer_name"]
                    row[head.split("-")[0] + "_rate"] = head.split("-")[1]
                    row[head.split("-")[0] + "_amount"] = invoices[inv]["taxes"][head][
                        "tax"
                    ]
                    total_tax += invoices[inv]["taxes"][head]["tax"]
                    row["taxable_amount"] = invoices[inv]["taxes"][head]["taxable"]
                    hsns.extend(invoices[inv]["taxes"][head]["hsns"])
            hsns = [hsn for hsn in hsns if hsn is not None]

            row["hsns"] = ",".join(list(set(hsns)))
            row["total_tax"] = total_tax
            row["net_total"] = row["taxable_amount"] + total_tax
            if row_include:
                data.append(row)

    return columns, data


def get_conditions(filters):
    """Get Filter Items"""
    conditions = ""
    for opts in (
        ("company", " and sinv.company=%(company)s"),
        ("from_date", " and sinv.posting_date>=%(from_date)s"),
        ("to_date", " and sinv.posting_date<=%(to_date)s"),
    ):
        if filters.get(opts[0]):
            conditions += opts[1]
    return conditions


def get_invoice_item_tax_map(invoice_list):
    import json

    invoices_data = {}

    if len(invoice_list) > 0:
        invoices_str = ",".join(["'%s'" % (inv) for inv in invoice_list])
        tax_details = frappe.db.sql(
            f"""select parent as invoice, account_head, item_wise_tax_detail
            from `tabSales Taxes and Charges` where parent in ({invoices_str})"""
        )
        for invoice, account_head, item_wise_tax_detail in tax_details:
            if invoice not in invoices_data:
                invoices_data.setdefault(invoice, {})

            tax_detail = json.loads(item_wise_tax_detail)
            gst_type = get_gst_type(account_head)

            if gst_type is None:
                continue
            for item in tax_detail:
                if item not in invoices_data[invoice]:
                    invoices_data[invoice].setdefault(item, {})
                if tax_detail[item][1] > 0:
                    invoices_data[invoice][item][
                        gstr(gst_type, tax_detail[item][0])
                    ] = tax_detail[item][1]

    return invoices_data


def get_gst_type(account_head):
    for gtype in GST_TYPES:
        if gtype in account_head:
            return gtype
    return None


def get_invoices(filters):
    conditions = get_conditions(filters)
    invoices_data = frappe.db.sql(
        """
		select sinv.name as invoice_no, sinv.customer_name, sinv.posting_date,
		sinv.taxes_and_charges, sitem.item_code,sitem.item_name,sitem.gst_hsn_code,sitem.net_amount as taxable,
		IFNULL(itemtaxtemp.name, 'NA') as item_tax_template, IFNULL(itemtaxtemp.cumulative_tax, 0)as tax_rate,
		(sitem.net_amount*IFNULL(itemtaxtemp.cumulative_tax, 0)/100) as tax
		from `tabSales Invoice` sinv
		join `tabSales Invoice Item` sitem
		on sitem.parent = sinv.name
		left join `tabItem Tax Template` itemtaxtemp
		on  itemtaxtemp.name = sitem.item_tax_template
		where sinv.docstatus = 1 %s order by posting_date desc, sinv.name desc"""
        % (conditions),
        filters,
        as_dict=0,
    )

    inv_item_tax_map = get_invoice_item_tax_map(
        list(set([inv[0] for inv in invoices_data]))
    )

    frappe.errprint(inv_item_tax_map)

    invoices = {}

    for (
        invoice_no,
        customer_name,
        posting_date,
        taxes_and_charges,
        item_code,
        item_name,
        gst_hsn_code,
        taxable,
        item_tax_template,
        tax_rate,
        tax,
    ) in invoices_data:
        if invoice_no not in invoices:
            invoices.setdefault(
                invoice_no,
                {
                    "details": {
                        "posting_date": posting_date,
                        "customer_name": customer_name,
                    },
                    "taxes": {},
                },
            )
        TAXABLE = taxable
        item_taxes = inv_item_tax_map[invoice_no][
            item_name if not item_code else item_code
        ]

        # Tax Free Item
        if not item_taxes:
            invoices[invoice_no]["taxes"].setdefault(
                "IGST-0.0", {"hsns": [], "taxable": 0, "tax": 0, "tax_rate": 0}
            )
            invoices[invoice_no]["taxes"]["IGST-0.0"]["taxable"] += taxable

            if (
                gst_hsn_code
                and gst_hsn_code
                not in invoices[invoice_no]["taxes"]["IGST-0.0"]["hsns"]
            ):
                invoices[invoice_no]["taxes"]["IGST-0.0"]["hsns"].append(gst_hsn_code)

        # With Tax Items
        for gtype in item_taxes:
            if gtype not in invoices[invoice_no]["taxes"]:
                invoices[invoice_no]["taxes"].setdefault(
                    gtype, {"hsns": [], "taxable": 0, "tax": 0, "tax_rate": 0}
                )
            if (
                gst_hsn_code
                and gst_hsn_code not in invoices[invoice_no]["taxes"][gtype]["hsns"]
            ):
                invoices[invoice_no]["taxes"][gtype]["hsns"].append(gst_hsn_code)
            invoices[invoice_no]["taxes"][gtype]["taxable"] += taxable
            invoices[invoice_no]["taxes"][gtype]["tax"] += item_taxes[gtype]
            frappe.errprint(invoices[invoice_no]["taxes"][gtype]["tax"])
    # frappe.errprint(invoices)
    return invoices


def gstr(tax_type, rate):
    return tax_type + "-" + str(rate)


def get_blank_row(inv):
    x = {"invoice": inv, "posting_date": "", "customer_name": ""}
    for gst_type in GST_TYPES:
        x.setdefault(gst_type + "_rate", 0)
        x.setdefault(gst_type + "_amount", 0)
    x.setdefault("total_tax", 0)
    x.setdefault("taxable_amount", 0)
    x.setdefault("net_total", 0)
    return x


def get_columns(filters):
    columns = [
        {
            "label": _("Invoice"),
            "fieldname": "invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 120,
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 80,
        },
        {
            "label": _("Customer Name"),
            "fieldname": "customer_name",
            "fieldtype": "Data",
            "width": 120,
        },
        {"label": _("HSNs"), "fieldname": "hsns", "fieldtype": "Data", "width": 200},
    ]
    tax_columns = [
        {
            "label": _("CGST Rate"),
            "fieldname": "CGST_rate",
            "fieldtype": "Percent",
            "width": 120,
        },
        {
            "label": _("CGST Amount"),
            "fieldname": "CGST_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "label": _("SGST Rate"),
            "fieldname": "SGST_rate",
            "fieldtype": "Percent",
            "width": 120,
        },
        {
            "label": _("SGST Amount"),
            "fieldname": "SGST_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "label": _("IGST Rate"),
            "fieldname": "IGST_rate",
            "fieldtype": "Percent",
            "width": 120,
        },
        {
            "label": _("IGST Amount"),
            "fieldname": "IGST_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
    ]

    total_columns = [
        {
            "label": _("Total Tax"),
            "fieldname": "total_tax",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "label": _("Taxable"),
            "fieldname": "taxable_amount",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
        {
            "label": _("Net Total"),
            "fieldname": "net_total",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
        },
    ]
    columns = columns + tax_columns + total_columns
    return columns
