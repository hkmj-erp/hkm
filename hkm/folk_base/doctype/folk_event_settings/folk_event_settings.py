# Copyright (c) 2023, Narahari Dasa and contributors
# For license information, please see license.txt

import frappe, json
from frappe.model.document import Document


class FOLKEventSettings(Document):
    pass


@frappe.whitelist()
def update_razorpay_entries():
    settings_doc = frappe.get_doc("FOLK Event Settings")
    from_time = datetime_to_timestamp(settings_doc.raz_from)
    to_time = datetime_to_timestamp(settings_doc.raz_to)
    import requests

    count = 100
    skip = 0

    data = []
    done = False
    while done == False:
        url = "https://api.razorpay.com/v1/payments/?count={}&skip={}&from={}&to={}".format(
            count, skip, int(from_time), int(to_time)
        )

        response = requests.get(
            url, auth=(settings_doc.key, settings_doc.get_password("secret"))
        )

        if response.status_code == 200:
            dt = json.loads(response.text)
            data.extend(dt["items"])
            skip += count
            if dt["count"] < 100:
                done = True
        else:
            break
    if data:
        for d in data:
            if d["amount"] == settings_doc.amount and d["status"] == "captured":
                # return ["reached", d]
                if not frappe.db.exists("FOLK Event Participant", d["order_id"]):

                    # doc = frappe.new_doc('FOLK Event Participant')

                    values = {
                        "doctype": "FOLK Event Participant",
                        "order_id": d["order_id"],
                    }
                    make_ready_doc(values, d, "name")
                    make_ready_doc(values, d, "mobile")
                    make_ready_doc(values, d, "email")
                    make_ready_doc(values, d, "institute")
                    make_ready_doc(values, d, "whatsapp_number")

                    doc = frappe.get_doc(values)

                    # doc.order_id = d['order_id']
                    # doc.student_name = d['notes']['name']
                    # doc.mobile_no = d['notes']['mobile']
                    # doc.email = d['notes']['email']
                    # if 'institute' in d['notes']:
                    # 	doc.institute = d['notes']['institute']
                    # if 'whatsapp_number' in d['notes']:
                    # 	doc.whatsapp_number = d['notes']['whatsapp_number']
                    doc.insert()
    frappe.db.commit()
    return True


def make_ready_doc(values, data, fieldname):
    alias = {"name": "student_name", "mobile": "mobile_no"}
    if fieldname in data["notes"]:
        if fieldname in alias:
            values[alias[fieldname]] = data["notes"][fieldname]
        else:
            values[fieldname] = data["notes"][fieldname]


from datetime import datetime


def datetime_to_timestamp(datetime_str):
    datetime_format = "%Y-%m-%d %H:%M:%S"
    datetime_object = datetime.strptime(datetime_str, datetime_format)
    timestamp = datetime_object.timestamp()
    return timestamp


def send_QR_whatsapp():
    return


def send_QR_mobile():
    return


@frappe.whitelist()
def send_QR_email():
    settings = frappe.get_doc("FOLK Event Settings")
    data = frappe.db.get_list(
        "FOLK Event Participant",
        filters={"student_name": ["is", "set"]},
        fields=["name", "student_name", "email", "email_sent"],
    )
    for d in data:
        if d["email_sent"] == 1 or not d["email"]:
            continue
        frappe.sendmail(
            sender="support@harekrishnajaipur.org",
            recipients=[d["email"]],
            subject=frappe._("Bonfire Event 2023"),
            template="bonfire_qr",
            args=dict(name=d["student_name"], qr_code=d["name"]),
            header=("Bonfire QR Code"),
        )
        frappe.db.set_value("FOLK Event Participant", d["name"], "email_sent", 1)

    frappe.db.commit()
