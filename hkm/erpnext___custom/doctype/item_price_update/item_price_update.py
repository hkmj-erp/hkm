# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class ItemPriceUpdate(Document):
    # begin: auto-generated types
    # This code is auto-generated. Do not modify anything in this block.

    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from frappe.types import DF
        from hkm.erpnext___custom.doctype.item_price_update_detail.item_price_update_detail import ItemPriceUpdateDetail

        amended_from: DF.Link | None
        company: DF.Link
        item_group: DF.Link | None
        items: DF.Table[ItemPriceUpdateDetail]
        name: DF.Int | None
        price_list: DF.Link
        scan_barcode: DF.Data | None
    # end: auto-generated types
    def validate(self):
        self.validate_duplicate()

    def validate_duplicate(self):
        documents = []
        for d in self.get("items"):
            if d.item_code in documents:
                frappe.throw(
                    "Row#{0} Duplicate record not allowed for {1}".format(
                        d.idx, d.item_code
                    )
                )

            documents.append(d.item_code)

    def on_submit(self):
        # Delete All Taxes Earlier Set
        for row in self.items:
            query = """
							delete tax
							from `tabItem Tax` tax
							join `tabItem` item on tax.parent = item.name
							join `tabItem Tax Template` temp on temp.name = tax.item_tax_template
							where temp.company = '{}' and item.name ='{}'
							""".format(
                self.company, row.item_code
            )
            frappe.db.sql(query)

            query = """
							delete price
							from `tabItem Price` price
							where item_code = '{}' and price_list = '{}'
							""".format(
                row.item_code, self.price_list
            )
            frappe.db.sql(query)

        frappe.db.commit()

        for row in self.items:
            if row.tax_template:
                item_doc = frappe.get_doc("Item", row.item_code)
                item_doc.append(
                    "taxes",
                    {"parent": row.item_code, "item_tax_template": row.tax_template},
                )
                item_doc.save(ignore_permissions=True)

            if row.price_rate:
                price_doc = frappe.get_doc(
                    {
                        "doctype": "Item Price",
                        "item_code": row.item_code,
                        "price_list": self.price_list,
                        "selling": 1,
                        "price_list_rate": row.price_rate,
                    }
                )
                price_doc.insert(ignore_permissions=True)


@frappe.whitelist()
def get_current_applied_tax_template(item_code, company):
    temps = frappe.db.sql(
        """
					select template.name as template, template.cumulative_tax as rate
					from `tabItem` item
					join `tabItem Tax` item_tax on item_tax.parent = item.name
					join `tabItem Tax Template` template on template.name = item_tax.item_tax_template
					where item.name = '{}' and template.company = '{}'
					""".format(
            item_code, company
        ),
        as_dict=1,
    )
    if len(temps) > 0:
        return temps[0]
    return None


@frappe.whitelist()
def get_current_applied_tax_template(item_code, company):
    temps = frappe.db.sql(
        """
					select template.name as template, template.cumulative_tax as rate
					from `tabItem` item
					join `tabItem Tax` item_tax on item_tax.parent = item.name
					join `tabItem Tax Template` template on template.name = item_tax.item_tax_template
					where item.name = '{}' and template.company = '{}'
					""".format(
            item_code, company
        ),
        as_dict=1,
    )
    if len(temps) > 0:
        return temps[0]
    return None
