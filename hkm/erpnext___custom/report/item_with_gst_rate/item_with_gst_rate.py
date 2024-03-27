# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe
from frappe.utils.nestedset import get_descendants_of


def execute(filters=None):
    columns, data = [], []

    if not filters:
        filters = {}
    columns = get_columns(filters)
    conditions = get_condition(filters)

    data_map = {}

    for i in frappe.db.sql(
        """
							SELECT
								item.`item_code` as item,
								item.`item_name` as item_name,
								item.`item_group` as item_group,
								item.`valuation_rate` as valuation_rate,
								item_price.`price_list_rate` as price_rate,
								template.name as tax_template,
								template.cumulative_tax as tax_rate,
								IF(STRCMP(template.name,"")=1,
									ROUND(item_price.`price_list_rate`+(item_price.`price_list_rate`* template.cumulative_tax/100),0), 
									ROUND(item_price.`price_list_rate`,0)
								) as sale_rate,
								item_barcode.barcode
							FROM
								`tabItem` item
							LEFT JOIN `tabItem Price` item_price
								ON item_price.item_code = item.name
							LEFT JOIN `tabItem Barcode` item_barcode
								ON item_barcode.parent = item.name
							LEFT JOIN `tabItem Tax` tax
								ON tax.parent = item.name
							LEFT JOIN `tabItem Tax Template` template
								ON tax.item_tax_template = template.name
							WHERE item.has_variants=0 and item.is_sales_item=1 %s
							"""
        % (conditions),
        filters,
        as_dict=1,
    ):
        if i.item in data_map:
            data_map[i.item]["barcode"] += "," + i["barcode"]
        else:
            data_map.setdefault(i.item, i)

    for d in sorted(data_map):
        data.append(
            [
                data_map[d]["item"],
                data_map[d]["barcode"],
                data_map[d]["item_name"],
                data_map[d]["item_group"],
                data_map[d]["valuation_rate"],
                data_map[d]["price_rate"],
                data_map[d]["tax_template"],
                data_map[d]["tax_rate"],
                {
                    "content": data_map[d]["sale_rate"],
                    "editable": 1,
                    # 'format': (value) => {
                    # 	return value.fontcolor('blue');
                    # }
                },
            ]
        )

    return columns, data


def get_condition(filters):
    conditions = ""

    if filters.get("item_group"):
        item_groups = get_descendants_of("Item Group", filters.get("item_group"))
        item_groups.append(filters.get("item_group"))
        if len(item_groups) > 1:
            conditions += " and item.item_group in {}".format(tuple(item_groups))
        else:
            conditions += " and item.item_group = %(item_group)s"
    for opts in (
        ("company", " and (template.name is null or template.company = %(company)s)"),
        ("price_list", " and item_price.price_list = %(price_list)s"),
    ):
        if filters.get(opts[0]):
            conditions += opts[1]

    return conditions


def get_columns(filters):
    columns = [
        {
            "fieldname": "item",
            "label": "Item",
            "fieldtype": "Link",
            "options": "Item",
            "width": 130,
        },
        {"fieldname": "barcode", "label": "Barcode", "fieldtype": "Data", "width": 120},
        {
            "fieldname": "item_name",
            "label": "Item Name",
            "fieldtype": "Data",
            "width": 250,
        },
        {
            "fieldname": "item_group",
            "label": "Item Group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 200,
        },
        {
            "fieldname": "valuation",
            "label": "Valuation",
            "fieldtype": "Currency",
            "width": 90,
        },
        {
            "fieldname": "price_rate",
            "label": "Price Rate",
            "fieldtype": "Currency",
            "width": 90,
        },
        {
            "fieldname": "tax_template",
            "label": "Tax Template",
            "fieldtype": "Link",
            "options": "Item Tax Template",
            "width": 150,
        },
        {"fieldname": "tax_rate", "label": "Tax Rate", "fieldtype": "Int", "width": 80},
        {
            "fieldname": "sale_rate",
            "label": "Sale Rate",
            "fieldtype": "Currency",
            "width": 100,
        },
    ]
    return columns
