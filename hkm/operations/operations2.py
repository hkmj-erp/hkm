from hkm.erpnext___custom.constants.custom_fields import CUSTOM_FIELDS
import frappe
from datetime import date
from frappe import enqueue
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
from frappe.utils.nestedset import get_descendants_of
from frappe.utils import add_to_date, now


@frappe.whitelist()
def query():
    # custom_fields_download()
    # return update_asset_data()
    # update_total_debit_credit()
    return
    # update_taxes()
    # return update_item_types_of_materi_request_items()

    # delete_two_entries()
    # query_specific()

    # update_folk_donation()
    # update_all_trashed_po()
    # enqueue('custom_app.modification.operations.update_folk_student_name')
    # update_folk_student_name()
    # return connect_mysql()
    return


def custom_fields_download():
    create_custom_fields(CUSTOM_FIELDS, update=True)


def update_asset_data():
    category_details = {}
    for c in frappe.db.get_all("Asset Category", fields="*"):
        category = frappe.get_doc("Asset Category", c)
        if len(category.finance_books) > 0:
            details = category.finance_books[0]
            category_details.setdefault(c["name"], details.as_dict())
    # return category_details
    for a in frappe.db.get_all(
        "Asset",
        filters={
            "docstatus": 0,
        },
        fields=["name", "asset_category"],
    ):
        if a["asset_category"] in category_details:
            asset = frappe.get_doc("Asset", a["name"])
            if len(asset.finance_books) == 0:
                asset.available_for_use_date = asset.purchase_date
                asset.append(
                    "finance_books",
                    {
                        "finance_book": category_details[asset.asset_category][
                            "finance_book"
                        ],
                        "depreciation_method": category_details[asset.asset_category][
                            "depreciation_method"
                        ],
                        "total_number_of_depreciations": category_details[
                            asset.asset_category
                        ]["total_number_of_depreciations"],
                        "frequency_of_depreciation": category_details[
                            asset.asset_category
                        ]["frequency_of_depreciation"],
                        "depreciation_start_date": add_to_date(
                            asset.purchase_date, days=1
                        ),
                    },
                )
            # asset.docstatus = 1
            asset.submit()
    frappe.db.commit()
    # return categories


def match_suspense():
    frappe.db.sql(
        """
						
					"""
    )


def update_total_debit_credit():
    entries = frappe.get_all(
        "Journal Entry", fields=["name"], filters={"total_debit": 0}
    )

    return entries
    for e in entries:
        total = 0
        je = frappe.get_doc("Journal Entry", e)
        for a in je.accounts:
            total += a.debit
        frappe.db.set_value("Journal Entry", e, "total_debit", total)
        frappe.db.set_value("Journal Entry", e, "total_credit", total)
    frappe.db.commit()


def update_taxes():
    import re

    parent_item_groups = {"BBT": "BBT"}

    for parent_item_group, tax_title in parent_item_groups.items():
        children_groups = get_descendants_of("Item Group", parent_item_group)
        children_groups.append(parent_item_group)
        items = []
        query = """select item.name,tax.item_tax_template,tax.name as tax_name
						from `tabItem` item
						join `tabItem Group` item_group
						on item.item_group = item_group.name
						join `tabItem Tax` tax
						on tax.parent = item.name
						where item_group.name in {}
						""".format(
            tuple(children_groups)
        )
        items = frappe.db.sql(query, as_dict=1)

        for item in items:
            tax_rate = (re.findall("[0-9]+", item["item_tax_template"]))[0]
            new_tax_template = "{} - {}% - TSFJ".format(tax_title, tax_rate)
            frappe.db.set_value(
                "Item Tax", item["tax_name"], "item_tax_template", new_tax_template
            )
    frappe.db.commit()
    return "success"


def update_item_types_of_materi_request_items():
    items = frappe.db.get_all(
        "Item", fields=["item_code", "is_stock_item", "is_fixed_asset"]
    )
    item_map = {}
    for item in items:
        item_map[item["item_code"]] = frappe._dict(
            is_stock_item=item["is_stock_item"], is_fixed_asset=item["is_fixed_asset"]
        )
    mr_items = frappe.db.get_all("Material Request Item", pluck="item_code")

    unique_items = list(set(mr_items))

    for item in unique_items:
        if item in item_map:
            item_type = get_item_type(item_map[item])
            frappe.db.sql(
                """
							UPDATE `tabMaterial Request Item`
							SET item_type = '{}'
							WHERE  item_code = '{}'
							""".format(
                    item_type, item
                )
            )
            frappe.db.sql(
                """
							UPDATE `tabPurchase Order Item`
							SET item_type = '{}'
							WHERE  item_code = '{}'
							""".format(
                    item_type, item
                )
            )

    frappe.db.commit()

    return unique_items


def get_item_type(item_details):
    if item_details["is_fixed_asset"] == 1:
        return "Asset"
    if item_details["is_stock_item"] == 1:
        return "Stock"
    return "Non-Stock"


def update_all_trashed_po():
    pos = frappe.db.sql(
        """
		select po.name
		from `tabPurchase Order` po
		join `tabToDo` todo on todo.reference_name = po.name
		where po.workflow_state = 'Trashed'
		group by po.name
		""",
        as_dict=0,
    )  #
    for po in pos:
        frappe.db.sql(
            """
				UPDATE `tabToDo`
				SET status = 'Cancelled'
				WHERE status = 'Open'
				AND reference_name = '{}'
				AND reference_type = 'Purchase Order'
				""".format(
                po[0]
            )
        )
    frappe.db.commit()
    return pos


def update_folk_student_name():
    folk_students = frappe.get_all(
        "FOLK Student",
        fields=["name", "student_mobile_number"],
        filters={"name": ["like", "%KS%"]},
    )
    for std in folk_students:
        frappe.rename_doc("FOLK Student", std["name"], std["student_mobile_number"])
        frappe.db.commit()


# Operation - Update all FOLK Donation with FOLK Guide Value


def update_folk_donation():
    donations = frappe.get_all("FOLK Donation", fields=["name", "folk_student"])
    for d in donations:
        std = frappe.get_doc("FOLK Student", d["folk_student"])
        frappe.db.set_value("FOLK Donation", d["name"], "folk_guide", std.folk_guide)

    frappe.db.commit()


def update_items():
    app_items = []

    items = frappe.get_all("Temp TSF HSN", fields=["name", "hsn", "rate"])

    for item in items:
        siblings = getSiblings(item["name"])
        for s in siblings:
            app_items.append(
                {
                    "name": s,
                    "hsn": int(item["hsn"]),
                    "rate": int(item["rate"]),
                }
            )
    app_items = getUniqueItems(app_items)
    updateItems(app_items)

    return app_items


def updateItems(items):
    for item in items:
        doc = frappe.get_doc("Item", item["name"])
        if item["hsn"] != 0:
            doc.gst_hsn_code = item["hsn"]
        old_rate = 0
        if doc.taxes != []:
            old_rate = int(list(doc.taxes[0].item_tax_template.split(" "))[-1])
        doc.set("taxes", [])
        if item["rate"] != 0:
            doc.append(
                "taxes", {"item_tax_template": "TSF GST {}".format(item["rate"])}
            )

        doc.save()
        frappe.db.commit()

        if doc.has_variants != 1:
            prices = frappe.get_all(
                "Item Price",
                filters={"item_code": doc.name, "price_list": "Standard Selling"},
                fields=["name", "price_list_rate"],
            )
            for price in prices:
                old_price = price["price_list_rate"]
                cur_rate = item["rate"]
                cur_price = old_price * ((100 + old_rate) / (100 + cur_rate))
                frappe.db.set_value(
                    "Item Price", price["name"], "price_list_rate", cur_price
                )


def getUniqueItems(items):
    result = []

    for item in items:
        found = 0
        for r in result:
            if item["name"] == r["name"]:
                found = 1
                r["rate"] = max(item["rate"], r["rate"])
                break
        if found == 0:
            result.append(item)
    return result


def getSiblings(name):
    sbls = []
    doc = frappe.get_doc("Item", name)
    if doc.variant_of is not None:
        parent = doc.variant_of
        sbls.extend(
            frappe.get_all("Item", filters={"variant_of": doc.variant_of}, pluck="name")
        )
        sbls.append(parent)
    else:
        sbls.append(doc.name)
    return sbls
    # items = frappe.db.sql("""
    # 	SELECT DISTINCT `tabItem`.`name`
    # 	FROM `tabItem`
    # 	JOIN `tabItem Price`
    # 	ON `tabItem Price`.item_code = `tabItem`.name
    # 	WHERE 1
    # 	""",as_dict=1)
    # pricesp = []
    # maxp =[]
    # for item in items:
    # 	prices = frappe.db.sql("""
    # 				SELECT `name`,`price_list_rate`,`item_code`
    # 				FROM `tabItem Price`
    # 				WHERE `tabItem Price`.item_code = '{}'
    # 				AND selling = 1
    # 				""".format(item['name']),as_dict=1)
    # 	if len(prices) > 1:
    # 		pricesp.append(prices)
    # 		maxPricedItem = max(prices, key=lambda x:x['price_list_rate'])
    # 		maxp.append(maxPricedItem)
    # 		for price in prices:
    # 			if price['name'] != maxPricedItem['name']:
    # 				# frappe.delete_doc('Item Price', price['name'])
    # 				frappe.db.sql("""
    # 					DELETE FROM `tabItem Price`
    # 					WHERE name = '{}';
    # 					""".format(price['name']))
    # 				frappe.db.commit()
    # return(pricesp,maxp)
    # doc = frappe.get_doc('POS Closing Entry','POS-CLO-2021-00076')
    # return doc.pos_transactions
    # candidates = frappe.db.sql("""
    # 	SELECT `name`
    # 	FROM `tabAshraya Candidate`
    # 	WHERE 1
    # 	""",as_dict=1)
    # for candidate_id in candidates:
    # 	latest_ashraya = frappe.db.sql("""
    # 						SELECT acp.level
    # 						FROM `tabAshraya Candidate` as ac
    # 						JOIN
    # 						(
    # 							SELECT `tabAshraya Ceremony Participant`.participant ,`tabAshraya Ceremony`.date, `tabAshraya Ceremony Participant`.level, `tabAshraya Level`.level_index
    # 							FROM `tabAshraya Ceremony Participant`
    # 							JOIN `tabAshraya Level`
    # 							ON `tabAshraya Ceremony Participant`.level = `tabAshraya Level`.name
    # 							JOIN `tabAshraya Ceremony`
    # 							ON `tabAshraya Ceremony Participant`.ashraya_ceremony = `tabAshraya Ceremony`.name
    # 						) as acp
    # 						ON acp.participant = ac.name
    # 						WHERE ac.name = '{}'
    # 						ORDER BY level_index DESC
    # 						LIMIT 1
    # 						""".format(candidate_id['name']))
    # 	if len(latest_ashraya) > 0 and len(latest_ashraya[0]) > 0:
    # 		frappe.db.sql("""
    # 			UPDATE `tabAshraya Candidate`
    # 			SET latest_level_of_ashraya = '{}'
    # 			WHERE `tabAshraya Candidate`.name = '{}'
    # 			""".format(latest_ashraya[0][0],candidate_id['name']))
    # 	frappe.db.commit()
    # data = frappe.db.sql("""
    #     SELECT
    #        	`item_code`,`item_name`,`item_tax_template`,itax.`name` as tax_name
    #     FROM `tabItem` item
    #     JOIN `tabItem Tax` itax
    #         ON itax.parent = item.name
    # """, values={}, as_dict=1) #-- WHERE gl.company = %(company)s
    # for row in data:
    # 	if "TSF GST" in row['item_tax_template']:
    # 		frappe.db.set_value('Item Tax', row['tax_name'], 'tax_category', '')
    # 		#frappe.db.delete('Item Tax', {'name': row['tax_name']})
    # # frappe.db.commit()
    # # for item in data:
    # # 	doc = frappe.get_doc('Item', item['item_code'])
    # # 	if len(doc.taxes)==1:
    # # 		if "TSF" in doc.taxes[0].item_tax_template:
    # # 			first_tax = doc.taxes[0].item_tax_template
    # # 			new_tax = frappe.get_doc(
    # # 				doctype='Item Tax',
    # # 				item_tax_template='TSF IGST '+lastWord(first_tax)+' - TSFJ',
    # # 				parent = item['item_code'],
    # # 				parentfield= "taxes",
    # # 				parenttype= "Item",
    # # 				tax_category= "Out of State"
    # # 				)
    # # 			new_tax.insert() idx
    # frappe.db.commit()
    # return data


def lastWord(string):
    # split by space and converting
    # string to list and
    lis = list(string.split(" "))

    # length of list
    length = len(lis)

    # returning last element in list
    return lis[length - 1]


def update_stock_ledger_gl_entries(voucher_no):
    gl_entries = frappe.db.sql(
        """
								select * from `tabGL Entry` where voucher_no = '{}'
								""".format(
            voucher_no
        )
    )


def query_specific():
    blocks = [
        ("SINV-21-00310", 771.5),
        ("SINV-21-00311", 2911.47),
        ("SINV-21-00313", 836.5),
        ("SINV-21-00314", 2494.7),
        ("SINV-21-00316", 2869.75),
        ("SINV-21-00318", 5398),
        ("SINV-21-00319", 1649.76),
        ("SINV-21-00322", 2468.76),
        ("SINV-21-00321", 551.5),
    ]

    for block in blocks:
        voucher_no, amount = block[0], block[1]

        current_doc = frappe.get_doc("Sales Invoice", voucher_no)
        # Create Cost of Good Sold
        create_a_GL_Entry(
            current_doc, "Cost of Goods Sold - TSFJ", "Stock In Hand - TSFJ", amount, 0
        )
        create_a_GL_Entry(
            current_doc, "Stock In Hand - TSFJ", "Cost of Goods Sold - TSFJ", 0, amount
        )
        frappe.db.commit()


def create_a_GL_Entry(doc, account, against, debit, credit):
    gl_doc = frappe.get_doc(
        {
            "doctype": "GL Entry",
            "posting_date": doc.posting_date,
            "account": account,
            "cost_center": "Main - TSFJ",
            "debit": debit,
            "debit_in_account_currency": debit,
            "credit": credit,
            "credit_in_account_currency": credit,
            "against": against,
            "voucher_type": doc.doctype,
            "voucher_no": doc.name,
            "company": doc.company,
        }
    )
    gl_doc.save(ignore_permissions=True)
    # frappe.get_doc("Sales Invoice",{})


def delete_two_entries():
    frappe.db.sql(
        """DELETE FROM `tabGL Entry` WHERE name = '{}'""".format("9c2aaa3a3d")
    )
    frappe.db.sql(
        """DELETE FROM `tabGL Entry` WHERE name = '{}'""".format("5013f4f9be")
    )
    frappe.db.commit()


vec = []
depth = 1
max_depth = 0


def demo():
    accounts = frappe.db.get_all(
        "Account",
        fields=["name", "is_group", "parent_account"],
        filters={"company": "Hare Krishna Movement Jaipur"},
    )
    final_data = []

    root = "Application of Funds (Assets) - HKMJ"

    def generate_accounts(root):
        if root is None:
            return

        global vec
        global depth
        global max_depth
        vec.append(root)
        depth = depth + 1

        c_accounts = [a["name"] for a in accounts if a["parent_account"] == root]
        if len(c_accounts) == 0:
            fill_data(vec)
            vec.pop()
            depth = depth - 1
            if depth > max_depth:
                max_depth = depth + 1
            return
        else:
            for index, account in enumerate(c_accounts):
                generate_accounts(account)
        vec.pop()
        depth = depth - 1

    root_accounts = []
    for account in accounts:
        if account["parent_account"] is None:
            root_accounts.append(account["name"])

    def fill_data(vec):
        row = []
        for ele in vec:
            row.append(ele)
        final_data.append(row)

    for r_account in root_accounts:
        generate_accounts(r_account)
    # return final_data
    i = 0
    # while i<=max_depth:
    # 	columns.append("D{}".format(i))
    for d in final_data:
        extra = [""] * (max_depth - len(d) + 1)
        d.extend(extra)

    return final_data
