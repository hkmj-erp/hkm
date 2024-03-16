import json
import re
from dhananjaya.dhananjaya.api.v3.marketing.identify import identify_donor
import frappe
from datetime import date
from frappe import enqueue
from frappe.utils.nestedset import get_descendants_of
from frappe.utils import add_to_date, now
from frappe.desk.page.setup_wizard.setup_wizard import make_records
from frappe.custom.doctype.custom_field.custom_field import create_custom_fields
import calendar

# def cash_entries_adjust():
# 	query = """
# 			SELECT tdr.name as receipt, tdr.amount as Amount
# 			FROM `tabDonation Receipt` tdr
# 			LEFT JOIN `tabJournal Entry` tje
# 			ON tje.donation_receipt  = tdr.name
# 			WHERE tdr.docstatus = 1
# 			AND tdr.payment_method  = "Cash"
# 			AND tje.name IS NULL
# 			AND tdr.receipt_date >= "2023-04-01"
# 			AND tdr.company = "Hare Krishna Movement Jaipur"
# 			"""
# 	for r in frappe.db.sql(query=query,as_dict=1):
# 		cash_journal_entry(r['receipt'])
# 	frappe.db.commit()

# def cash_journal_entry(receipt_number):
# 	receipt_doc = frappe.get_doc("Donation Receipt",receipt_number)
# 	seva_type_doc = frappe.get_cached_doc("Seva Type", receipt_doc.seva_type)

# 	default_cost_center = receipt_doc.get_cost_center()

# 	je = {
# 		"doctype": "Journal Entry",
# 		"voucher_type": "Cash Entry",
# 		"company": receipt_doc.company,
# 		"donation_receipt": receipt_doc.name,
# 		"docstatus": 1,
# 	}

# 	##### In Case of New Donor Request #####

# 	if not receipt_doc.donor:
# 		if not receipt_doc.donor_creation_request:
# 			frappe.throw(
# 				"At least one of Donor or Donation Creation Request document is must to process."
# 			)
# 		donor_name = frappe.get_value(
# 			"Donor Creation Request", receipt_doc.donor_creation_request, "full_name"
# 		)
# 	else:
# 		donor_name = receipt_doc.full_name

# 	########################################

# 	je.setdefault(
# 		"user_remark",
# 		f"BEING AMOUNT RECEIVED FOR {receipt_doc.seva_type} FROM {donor_name} AS PER R.NO.{receipt_doc.name} DT:{receipt_doc.receipt_date} {receipt_doc.preacher} ",
# 	)

# 	# Jounrnal Entry date should be the day Cashier received the amount because it has to tally with Cashbook.
# 	cash_date = receipt_doc.modified

# 	je.setdefault("posting_date", cash_date)
# 	je.setdefault(
# 		"accounts",
# 		[
# 			{
# 				"account": receipt_doc.donation_account,
# 				"credit_in_account_currency": receipt_doc.amount,
# 				# This is needed for cost center analysis.
# 				"cost_center": default_cost_center,
# 			},
# 			{
# 				"account": receipt_doc.cash_account,
# 				"debit_in_account_currency": receipt_doc.amount,
# 				# As it not compulsory. It will pick up the default.--> But now it is picking of other company, so explicitly declared.
# 				"cost_center": default_cost_center,
# 			},
# 		],
# 	)
# 	je_doc = frappe.get_doc(je)
# 	je_doc.insert()


def notifiy_users_of_new_version():
    users = frappe.get_all(
        "Firebase App Token", filters={"app": "Dhananjaya"}, pluck="user"
    )
    users = list(set(users))
    for user in users:
        message = f"""Starting soon, we're switching to OTP login for simplicity.\n\nRemember, your registered email is {user}\n\nMake sure you have access to it for OTPs.\n\nNext App Update will be released on 12th March | 07:00 PM.
					"""
        doc = frappe.get_doc(
            {
                "doctype": "App Notification",
                "app": "Dhananjaya",
                "user": user,
                "subject": "Important Update!",
                "message": message,
            }
        )
        doc.insert(ignore_permissions=True)
    frappe.db.commit()


def ahmd_mobile_clean():
    frappe.db.sql("Donor Contact")


def import_special_pujas():
    for idx, d in enumerate(frappe.get_all("Temp Data", fields="*")):
        if d["value_set"]:
            continue
        if not d["occasion"]:
            continue
        print(f"Processing {idx}")
        if len(d["mobile"]) < 15:
            clean_contact = re.sub(r"\D", "", d["mobile"])
            clean_contact = clean_contact[-10:]
        else:
            contacts = []
            # if " " in d["mobile"]:
            #     contacts = d["mobile"].split(" ")
            # for contact in contacts:
            clean_contact = re.sub(r"\D", "", d["mobile"])[:10]
            print(clean_contact)
            donor = identify_donor(
                contact=clean_contact, email=None, pan=None, aadhar=None
            )
            if donor:
                donor = frappe.get_doc("Donor", donor)
                donor.append(
                    "puja_details",
                    {
                        "day": d["day"],
                        "month": calendar.month_name[int(d["month"])],
                        "occasion": d["occasion"],
                    },
                )
                print(f"Saving Donor{donor.name}")
                donor.save()
                frappe.db.set_value("Temp Data", d["name"], "value_set", 1)
                # break
        frappe.db.commit()


def create_seva_type():
    for s in frappe.db.sql(
        "SELECT company,seva_type FROM `tabDonation Receipt` WHERE seva_type IS NOT NULL GROUP BY company,seva_type"
    ):
        if not frappe.db.exists("Seva Type", {"company": s[0], "seva_name": s[1]}):
            doc = frappe.get_doc(
                {
                    "doctype": "Seva Type",
                    "company": s[0],
                    "seva_name": s[1],
                    "80g_applicable": 1,
                    # 'patronship_allowed':1,
                    "include_in_analysis": 1,
                    # 'csr_allowed':1
                }
            )
            doc.insert()
    frappe.db.commit()


def create_seva_subtype():
    for s in frappe.db.sql(
        "SELECT seva_subtype FROM `tabDonation Receipt` WHERE seva_subtype IS NOT NULL GROUP BY seva_subtype"
    ):
        if not frappe.db.exists("Seva Subtype", {"seva_name": s[0]}):
            doc = frappe.get_doc(
                {
                    "doctype": "Seva Subtype",
                    # "company": s[0],
                    "seva_name": s[0],
                    "80g_applicable": 1,
                    # 'patronship_allowed':1,
                    "include_in_analysis": 1,
                    # 'csr_allowed':1
                }
            )
            doc.insert()
    frappe.db.commit()


def set_seva_type():
    for r in frappe.get_all(
        "Donation Receipt",
        filters={
            "company": "Hare Krishna Movement Vrindavan",
            "seva_type": ["is", "not set"],
        },
        pluck="name",
    ):
        print(r)
        frappe.db.set_value("Donation Receipt", r, "seva_type", "GEN - HKMV")

    for r in frappe.get_all(
        "Donation Receipt",
        filters={
            "company": "Vrindavan Chandrodaya Mandir Trust",
            "seva_type": ["is", "not set"],
        },
        pluck="name",
    ):
        frappe.db.set_value("Donation Receipt", r, "seva_type", "GNRL - VCMT")

    frappe.db.commit()


def set_seva_type_for_no_company_tagged():
    companies_abbr = {}
    for c in frappe.get_all("Company", fields=["company_name", "abbr"]):
        companies_abbr.setdefault(c["company_name"], c["abbr"])
    for r in frappe.get_all(
        "Donation Receipt", fields=["name", "seva_type", "company"]
    ):
        if r["seva_type"] and "-" not in r["seva_type"]:
            new_seva_type = r["seva_type"] + " - " + companies_abbr[r["company"]]
            frappe.db.set_value("Donation Receipt", r, "seva_type", new_seva_type)
    frappe.db.commit()


def set_full_name():
    for r in frappe.get_all(
        "Donation Receipt",
        fields=["name", "donor"],
    ):
        full_name = frappe.db.get_value("Donor", r["donor"], "full_name")
        frappe.db.set_value("Donation Receipt", r, "full_name", full_name)

    frappe.db.commit()


def correct_names_patron():
    # for p in frappe.get_all("Patron",pluck = "name"):
    #     patron_doc = frappe.get_doc("Patron",p)
    #     patron_doc.first_name = patron_doc.first_name + " "
    #     patron_doc.save()
    # frappe.db.commit()
    for p in frappe.get_all("Patron Privilege Puja", pluck="name"):
        puja_doc = frappe.get_doc("Patron Privilege Puja", p)
        puja_doc.occasion = puja_doc.occasion + " "
        puja_doc.save()
    frappe.db.commit()
    for p in frappe.get_all("Patron Privilege Puja", pluck="name"):
        puja_doc = frappe.get_doc("Patron Privilege Puja", p)
        puja_doc.occasion = puja_doc.occasion.strip()
        puja_doc.save()
    frappe.db.commit()


@frappe.whitelist()
def query():
    pass
    # return update_depreciations()
    # update_barcodes()
    # update_special_pujas()
    # return upload_mumbai_data()
    # update_current_preacher()
    return


def update_depreciations():
    for temp_entry in frappe.get_all("Temp Data", fields=["*"]):
        asset_doc = frappe.get_doc("Asset", temp_entry["asset_id"])
        asset_location = asset_doc.location
        if asset_doc.docstatus == 1:
            cancel_dependent_asset_docs(asset_doc)
            asset_doc.reload()
            asset_doc.cancel()
        asset_doc.reload()
        duplicate_asset = frappe.copy_doc(doc=asset_doc)
        duplicate_asset.location = asset_location
        if duplicate_asset.available_for_use_date is None:
            duplicate_asset.available_for_use_date = duplicate_asset.purchase_date
        duplicate_asset.finance_books[0].depreciation_start_date = temp_entry[
            "depreciation_posting_date"
        ]
        duplicate_asset.finance_books[0].total_number_of_depreciations = temp_entry[
            "total_number_of_dep"
        ]
        duplicate_asset.finance_books[0].frequency_of_depreciation = temp_entry[
            "frequency_of_dep"
        ]
        duplicate_asset.save()
        duplicate_asset.submit()
        frappe.rename_doc(
            "Asset", duplicate_asset.name, asset_doc.name + "-1", merge=False
        )
        frappe.db.commit()


def cancel_dependent_asset_docs(asset_doc):
    jeas = frappe.get_all(
        "Journal Entry Account",
        filters=[
            ["docstatus", "=", 1],
            ["reference_name", "=", asset_doc.name],
            ["account", "LIKE", "%Accumulated Depreciations%"],
        ],
        pluck="parent",
    )
    journal_entries = list(set(jeas))
    for j in journal_entries:
        frappe.get_doc("Journal Entry", j).cancel()

    for m in frappe.get_all(
        "Asset Movement Item",
        filters=[["docstatus", "=", 1], ["asset", "=", asset_doc.name]],
        pluck="parent",
    ):
        frappe.get_doc("Asset Movement", m).cancel()


@frappe.whitelist()
def fetch_successful_docs(doctype):
    docs = frappe.get_all(
        "Data Migration Success", filters={"document_type": doctype}, pluck="docname"
    )
    return docs


@frappe.whitelist()
def create_document():
    data = json.loads(frappe.request.data)
    # frappe.local.response.update({"request":data})

    # insert document from request data
    doc = frappe.get_doc(data).insert(ignore_links=True, ignore_mandatory=True)

    # set response data
    frappe.local.response.update({"data": doc.as_dict()})

    if doc.name != data["name"]:
        frappe.rename_doc(data["doctype"], doc.name, data["name"], merge=False)

    # commit for POST requests
    frappe.db.commit()


def update_barcodes():
    for item in frappe.get_all(
        "Item", fields=["item_code"], filters=[["is_sales_item", "=", "1"]]
    ):
        item_doc = frappe.get_doc("Item", item["item_code"])
        found = False
        for b in item_doc.barcodes:
            if b.barcode == item_doc.item_code:
                found = True
                break
        if not found:
            item_doc.append("barcodes", {"barcode": item_doc.name})
            item_doc.save()
            frappe.db.commit()


def update_special_pujas():
    datas = frappe.get_all("Temp Data", fields=["*"])
    for data in datas:
        if data["mobile"]:
            clean_contact = re.sub(r"\D", "", data["mobile"])[-10:]
            contacts = frappe.db.sql(
                f"""
					select contact_no,parent
					from `tabDonor Contact`
					where REGEXP_REPLACE(contact_no, '[^0-9]+', '') LIKE '%{clean_contact}%' and parenttype = 'Donor'
					""",
                as_dict=1,
            )
            donor = None
            if len(contacts) > 0:
                donor = contacts[0]["parent"]
                donor_doc = frappe.get_doc("Donor", donor)
                if not data["date"]:
                    data["date"] = "NA"
                donor_doc.append(
                    "puja_details",
                    {
                        "month": data["donor"].strftime("%B"),
                        "day": data["donor"].day,
                        "occasion": data["date"],
                    },
                )
                donor_doc.save()

            if donor is not None:
                frappe.db.set_value("Temp Data", data["name"], "found", 1)
    frappe.db.commit()


# @frappe.whitelist()
def update_preacher_donor(d):
    max = frappe.db.sql(
        f"""
					SELECT preacher, count(*) as nos
					from `tabDonation Receipt` tdr 
					where donor = '{d}' AND receipt_date > NOW() - INTERVAL 3 YEAR  
					GROUP BY preacher
					order by nos desc, receipt_date desc
					"""
    )
    if len(max) > 0:
        max_preacher = max[0][0]
        if max_preacher is not None:
            frappe.db.set_value(
                "Donor", d, "llp_preacher", max_preacher, update_modified=False
            )
    else:
        latest_data = frappe.db.sql(
            f"""
				SELECT preacher,receipt_date
				FROM `tabDonation Receipt` tdr 
				WHERE donor = '{d}'
				order by receipt_date desc
				"""
        )
        if len(latest_data) > 0:
            frappe.db.set_value(
                "Donor", d, "llp_preacher", latest_data[0][0], update_modified=False
            )
    frappe.db.commit()


def cancel_dr():
    from dhananjaya.dhananjaya.doctype.donation_receipt.donation_receipt import (
        receipt_cancel_operations,
    )

    drs = frappe.get_all("Donation Receipt", filters={"is_ecs": 1}, pluck="name")
    for dr in drs:
        receipt_cancel_operations(dr)
    frappe.db.commit()


def journal_entry_preacher_update():
    import re

    jeas = frappe.get_all(
        "Journal Entry Account",
        filters={"is_a_donation": 1},
        fields=["parent", "devotee", "name", "dr_no"],
    )
    # return jeas
    pattern = r"^RC-\d{2}-\d{5}$"
    selected = []
    for jea in jeas:
        if jea.dr_no and (not jea.devotee) and re.match(pattern, str(jea.dr_no)):
            selected.append([jea.dr_no, jea.name, jea.parent])

    # return selected
    for s in selected:
        devotee = frappe.db.get_value("Donation Receipt", s[0], "preacher")

        if s[0] is None or devotee is None:
            return devotee, s

        frappe.db.set_value("Journal Entry Account", s[1], "devotee", devotee)

        statement = frappe.db.get_value("Journal Entry", s[2], "user_remark")
        pattern = r"None$"
        try:
            new_statement = re.sub(pattern, devotee, statement)
        except:
            return pattern, devotee, statement, s

        # return new_statement
        frappe.db.sql(
            f"""
						update `tabJournal Entry`
						set user_remark ='{new_statement}'
						where name = '{jea.parent}'
						"""
        )
        frappe.db.set_value("Journal Entry", s[2], "user_remark", new_statement)

    frappe.db.commit()
    # return selected, len(selected)
    # frappe.db.commit()


def get_donation_details():
    conditions = """
					AND tdr.receipt_date > NOW() - INTERVAL 10 year
					AND tdr.docstatus = 1
					AND tdr.seva_subtype NOT LIKE "%heri%"
					"""
    donors = {}
    for i in frappe.db.sql(
        f"""
					select tdr.donor as donor_id, tdr.receipt_date 
					from `tabDonation Receipt` tdr
					join (
						select tdr.donor, MAX(tdr.receipt_date) as last_donation_date
						from `tabDonation Receipt` tdr
						where 1 {conditions}
						group by donor
					) as last_donation_details
					on last_donation_details.donor = tdr.donor and tdr.receipt_date = last_donation_details.last_donation_date
					where 1 {conditions} AND tdr.preacher = 'PNVD'
					""",
        as_dict=1,
    ):
        donors.setdefault(i["donor_id"], i)

    donors_str = ",".join([f"'{k}'" for k in donors.keys()])

    for i in frappe.db.sql(
        f"""
					select
						tdr.donor as donor_id,
						tdr.full_name as donor_name, 
						sum(tdr.amount) as total_donation,
						count(tdr.name) as times,
						donor_details.contact,
						donor_details.address
						# MAX(tdr.receipt_date) as last_donation
					from `tabDonation Receipt` tdr
					join (
							select
								td.name as donor_id, td.full_name,
								GROUP_CONCAT(DISTINCT tc.contact_no SEPARATOR' , ') as contact,
								GROUP_CONCAT(DISTINCT ta.address_line_1,ta.address_line_2,ta.city SEPARATOR' | ') as address
							from `tabDonor` td
							left join `tabDonor Address` ta 
								on ta.parent = td.name
							left join `tabDonor Contact` tc 
								on tc.parent = td.name
							group by donor_id
						) as donor_details
						on donor_details.donor_id = tdr.donor 
					where tdr.donor IN ({donors_str})
					{conditions}
					group by tdr.donor
					order by times desc
					""",
        as_dict=1,
    ):
        donors[i["donor_id"]].update(i)

    for i in frappe.db.sql(
        f"""
							select 
								donor as donor_id,
								preacher,
								sum(tdr.amount) as total_donation,count(tdr.amount) as times
							from `tabDonation Receipt` tdr
							where 1 {conditions} AND tdr.donor IN ({donors_str})
							group by donor,preacher
							order by donor,total_donation desc
								""",
        as_dict=1,
    ):
        if not "top_collector" in donors[i["donor_id"]]:
            donors[i["donor_id"]].setdefault("top_collector", i["preacher"])
            donors[i["donor_id"]].setdefault(
                "top_collector_donation", i["total_donation"]
            )
            donors[i["donor_id"]].setdefault("top_collector_times", i["times"])
            continue
        if not "second_collector" in donors[i["donor_id"]]:
            donors[i["donor_id"]].setdefault("second_collector", i["preacher"])
            donors[i["donor_id"]].setdefault(
                "second_collector_donation", i["total_donation"]
            )
            donors[i["donor_id"]].setdefault("second_collector_times", i["times"])

    delets = []
    for d in donors:
        if "total_donation" not in donors[d]:
            delets.append(d)

    donors = {k: v for k, v in donors.items() if k not in delets}

    data = [v for k, v in donors.items()]
    headers = list(set().union(*data))
    # return headers
    from frappe.utils.xlsxutils import make_xlsx

    xlsx_data = [headers]

    for d in data:
        row = []
        for h in headers:
            if h in d:
                row.append(d[h])
            else:
                row.append("")
        xlsx_data.append(row)

    xlsx_file = make_xlsx(xlsx_data, "Donation Receipt")

    frappe.response["filename"] = "PNVD" + ".xlsx"
    frappe.response["filecontent"] = xlsx_file.getvalue()
    frappe.response["type"] = "binary"

    return xlsx_file


def create_donors_clear_suspense():
    all = frappe.get_all("Temp Data", fields="*")
    for index, a in enumerate(all):
        # if index > 100 and index <= 150:
        # if index:
        receipt = frappe.new_doc("Donation Receipt")
        receipt.update(
            {
                "naming_series": "RC-.YY.-1.####",
                "company": "Hare Krishna Movement Jaipur",
                "receipt_date": a["date"],
                "donor": a["donor"],
                "payment_method": "NEFT/IMPS",
                "amount": a["amount"],
                "seva_type": "GEN - HKMJ",
                "remarks": a["remarks"],
            }
        )
        if a["devotee"]:
            receipt.preacher = a["devotee"]
        receipt.save()

        frappe.db.set_value(
            "Donation Receipt",
            receipt.name,
            {"workflow_state": "Realized", "docstatus": 1},
        )

        je = {
            "voucher_type": "Journal Entry",
            "naming_series": "ACC-JV-.YYYY.-",
            "company": "Hare Krishna Movement Jaipur",
            # "temp_datetime":f"{dattime}",
            "posting_date": "2023-03-25",
            "cheque_no": a["remarks"],
            "cheque_date": f"{a['date']}",
            "user_remark": f"BEING AMOUNT RECEIVED FOR General Donation - HKMJ FROM {receipt.full_name} AS PER R.NO. {receipt.name} DT. {a['date']} {receipt.preacher}",
            "accounts": [
                {
                    "account": "Donation Income-India - HKMJ",
                    "devotee": f"{receipt.preacher}",
                    "cost_center": "General Donation - HKMJ",
                    "debit_in_account_currency": 0,
                    "debit": 0,
                    "credit_in_account_currency": a["amount"],
                    "credit": a["amount"],
                    "is_a_donation": 1,
                    "dr_no": receipt.name,
                    "donor_name": f"{receipt.full_name}",
                    "receipt_date": f"{a['date']}",
                },
                {
                    "account": "Suspense - HKMJ",
                    "cost_center": "Main - HKMJ",
                    "debit_in_account_currency": a["amount"],
                    "debit": a["amount"],
                    "credit_in_account_currency": 0,
                    "credit": 0,
                    "suspense_jv": a["suspense"],
                },
            ],
        }
        # je_doc = frappe.get_doc(je)
        # return je
        je_doc = frappe.new_doc("Journal Entry")
        je_doc.update(je)
        je_doc.save()
        je_doc.submit()

        frappe.db.commit()


def update_suspense():
    all = frappe.get_all("Temp Data", fields=["donation_jv", "bank_jv"])
    i = 1
    for a in all:
        frappe.db.sql(
            f"""
						update `tabJournal Entry Account`
						set suspense_jv = '{a["bank_jv"]}'
						where parent = '{a["donation_jv"]}' and account = 'Suspense - HKMJ'
						"""
        )
        # if i == 1:
        # 	break
    frappe.db.commit()


def make_custom_fields():
    custom_fields = {
        "Journal Entry": [
            dict(
                fieldname="donation_receipt",
                label="Donation Receipt",
                fieldtype="Link",
                options="Donation Receipt",
                insert_after="tax_withholding_category",
            ),
            dict(
                fieldname="bank_statement_name",
                label="Bank Statement Name",
                fieldtype="Data",
                insert_after="donation_receipt",
                hidden=1,
                read_only=1,
            ),
        ]
    }

    create_custom_fields(custom_fields)
    frappe.db.commit()
    return custom_fields


def update_current_preacher():
    donors = frappe.get_all("Donor", pluck="name")
    for d in donors:
        frappe.enqueue(
            update_preacher_donor,
            queue="long",
            job_name="Updating Preacher",
            timeout=1000000,
            d=d,
        )


# def update_preachers():
#     settings = frappe.get_cached_doc("Dhananjaya Import Settings")
#     companies = ",".join([str(c.old_trust_code) for c in settings.companies_to_import])
#     data = run_query(
#         f"""
#                     select DR_NUMBER,PREACHER_CODE
#                     from `view_receipt_details`
#                     where TRUST_ID IN ({companies})
#                     """
#     )
#     for d in data:
#         frappe.enqueue(
#             update_donation_receipt,
#             queue="long",
#             job_name="Updating Donor Receipt",
#             timeout=100000,
#             d=d,
#         )
# n = 10000
# chunks = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )]
# for ind, chunk in enumerate(chunks):
# 	frappe.enqueue(assign_chunk, queue='long',job_name=f"Assinging Chunk #{ind}",timeout=100000,chunk=chunk)
# # return chunks


def assign_chunk(chunk):
    for d in chunk:
        frappe.enqueue(
            update_donation_receipt,
            queue="long",
            job_name="Updating Donor Receipt",
            timeout=100000,
            d=d,
        )


def update_donation_receipt(d):
    frappe.db.sql(
        f"""
					update `tabDonation Receipt`
					set preacher = '{d['PREACHER_CODE']}'
					where old_dr_no = '{d['DR_NUMBER']}'
					"""
    )
    frappe.db.commit()


# def assign_
# 	frappe.enqueue(insert_a_donor, queue='short',job_name="Inserting Donor",timeout=100000,d=d)
# 	for d in data:
# 		frappe.db.sql(f"""
# 						update `tabDonation Receipt`
# 						set preacher = '{d['PREACHER_CODE']}'
# 						where old_dr_no = '{d['DR_NUMBER']}'
# 						""")
# 	frappe.db.commit()


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


def demo111():
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


# # def make_custom_records():
# 	records = [
# 		{'doctype': "Role", "role_name": "DCC Preacher"},
# 		{'doctype': "Role", "role_name": "DCC Executive"},
# 		{'doctype': "Role", "role_name": "DCC Manager"},
# 		{'doctype': "Role", "role_name": "DCC Cashier"}
# 	]
# 	records.extend(get_states_and_actions())
# 	if not frappe.db.exists("Workflow", "Donation Receipt Workflow"):
# 		records.append(get_workflow())
# 	make_records(records)


# def setup_dhananjaya():
# 	make_custom_records()
# 	make_custom_fields()
# 	frappe.db.commit()
# 	frappe.clear_cache()

# def make_custom_fields(update=True):
# 	custom_fields = get_custom_fields()
# 	create_custom_fields(custom_fields, update=update)


# def get_custom_fields():
# 	custom_fields = {
# 		'Journal Entry':[
# 			dict(fieldname ='donation_receipt', label ='Donation Receipt',
# 					fieldtype='Link',options='Donation Receipt',insert_after='bank_account')
# 		]
# 		# 'Company': [
# 		# 	dict(fieldname='dhananjaya_section', label='Dhananjaya Settings',
# 		# 		 fieldtype='Section Break', insert_after='asset_received_but_not_billed', collapsible=1),
# 		# 	dict(fieldname='dhananjaya_trust_code', label='Old Dhananjaya Trust Code',
# 		# 		 fieldtype='Data', insert_after='dhananjaya_section'),
# 		# 	dict(fieldname='c_80g_number', label='80G Number',
# 		# 		 fieldtype='Data', insert_after='dhananjaya_trust_code'),
# 		# 	dict(fieldname='pan_details', label='PAN Number',
# 		# 		 fieldtype='Data', insert_after='c_80g_number')
# 		# ]
# 	}
# 	return custom_fields

# def get_states_and_actions():
# 	return [
# 		## States ##
# 		{'doctype': "Workflow State", "workflow_state_name": "Light Blue"},
# 		{'doctype': "Workflow State", "workflow_state_name": "Acknowledged","style":"Dark Blue"},
# 		{'doctype': "Workflow State", "workflow_state_name": "Suspense", "style":"Warning"},
# 		{'doctype': "Workflow State", "workflow_state_name": "Received by Cashier", "style":"Success"},
# 		{'doctype': "Workflow State", "workflow_state_name": "Realized", "style":"Success"},
# 		{'doctype': "Workflow State", "workflow_state_name": "Cancelled","style":"Danger"},
# 		## Actions ##
# 		{'doctype': "Workflow Action Master", "workflow_action_name": "Acknowledge"},
# 		{'doctype': "Workflow Action Master", "workflow_action_name": "Receive Cash"},
# 		{'doctype': "Workflow Action Master", "workflow_action_name": "Confirm"},
# 		{'doctype': "Workflow Action Master", "workflow_action_name": "Cancel"},
# 	]
# def get_workflow():
# 	return {
# 				"workflow_name": "Donation Receipt Workflow",
# 				"document_type": "Donation Receipt",
# 				"is_active": 1,
# 				"override_status": 0,
# 				"send_email_alert": 0,
# 				"workflow_state_field": "workflow_state",
# 				"doctype": "Workflow",
# 				"transitions": [
# 									{
# 									"idx": 1,
# 									"state": "Draft",
# 									"action": "Acknowledge",
# 									"next_state": "Acknowledged",
# 									"allowed": "DCC Preacher",
# 									"allow_self_approval": 1,
# 									"condition": "doc.donor",
# 									"parent": "Donation Receipt Workflow",
# 									"parentfield": "transitions",
# 									"parenttype": "Workflow",
# 									"doctype": "Workflow Transition"
# 									},
# 									{
# 									"idx": 2,
# 									"state": "Acknowledged",
# 									"action": "Receive Cash",
# 									"next_state": "Received by Cashier",
# 									"allowed": "DCC Cashier",
# 									"allow_self_approval": 1,
# 									"parent": "Donation Receipt Workflow",
# 									"parentfield": "transitions",
# 									"parenttype": "Workflow",
# 									"doctype": "Workflow Transition"
# 									},
# 									{
# 									"idx": 3,
# 									"state": "Acknowledged",
# 									"action": "Confirm",
# 									"next_state": "Realized",
# 									"allowed": "DCC Executive",
# 									"allow_self_approval": 1,
# 									"parent": "Donation Receipt Workflow",
# 									"parentfield": "transitions",
# 									"parenttype": "Workflow",
# 									"doctype": "Workflow Transition"
# 									},
# 									{
# 									"idx": 4,
# 									"state": "Draft",
# 									"action": "Confirm",
# 									"next_state": "Suspense",
# 									"allowed": "DCC Executive",
# 									"allow_self_approval": 1,
# 									"condition": "not doc.donor",
# 									"parent": "Donation Receipt Workflow",
# 									"parentfield": "transitions",
# 									"parenttype": "Workflow",
# 									"doctype": "Workflow Transition"
# 									}
# 								],
# 				"states": [
# 							{
# 							"idx": 1,
# 							"state": "Draft",
# 							"doc_status": "0",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Preacher",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							},
# 							{
# 							"idx": 2,
# 							"state": "Acknowledged",
# 							"doc_status": "0",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Manager",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							},
# 							{
# 							"idx": 3,
# 							"state": "Received by Cashier",
# 							"doc_status": "1",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Manager",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							},
# 							{
# 							"idx": 4,
# 							"state": "Realized",
# 							"doc_status": "1",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Manager",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							},
# 							{
# 							"idx": 5,
# 							"state": "Suspense",
# 							"doc_status": "1",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Manager",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							},
# 							{
# 							"idx": 6,
# 							"state": "Cancelled",
# 							"doc_status": "2",
# 							"is_optional_state": 0,
# 							"allow_edit": "DCC Manager",
# 							"parent": "Donation Receipt Workflow",
# 							"parentfield": "states",
# 							"parenttype": "Workflow",
# 							"doctype": "Workflow Document State"
# 							}
# 						]
# 			}
