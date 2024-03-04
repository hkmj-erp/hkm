from hkm.erpnext___custom.doctype.whatsapp_settings.whatsapp_settings import (
    send_whatsapp_using_template,
)
import frappe
import random
import string

REDIS_PREFIX = "otp"


def random_string_generator(str_size, allowed_chars):
    return "".join(random.choice(allowed_chars) for x in range(str_size))


@frappe.whitelist(allow_guest=True)
def generate_otp(email):
    email = email.strip()
    if not frappe.db.exists("User", email):
        frappe.throw("No User exists with this Email")
    user = frappe.get_doc("User", email)
    phone = user.mobile_no
    key = f"{REDIS_PREFIX}:{email}"
    otp = None
    if frappe.cache().get(key):
        otp = frappe.cache().get(key).decode("utf-8")
    else:
        otp = random_string_generator(6, string.digits)
        frappe.cache().set(key, otp, ex=600)
    send_otp_on_email(email, otp)
    if phone:
        parameters = [
            {"type": "text", "text": otp},
            {"type": "text", "text": "Dhananjaya"},
        ]
        resp = send_whatsapp_using_template(
            phone, "mobile_app_authentication", parameters
        )
        print(resp)
    return


def send_otp_on_email(email, otp):
    frappe.sendmail(
        recipients=email,
        subject=f"OTP for Login into Mobile App!",
        message=f"Hare Krishna,<br>Please use the OTP below to login.<br><br><h4>{otp}</h4></a>",
        delayed=False,
    )


@frappe.whitelist(allow_guest=True)
def verify_otp(email, otp):
    key = f"{REDIS_PREFIX}:{email}"
    if not frappe.cache().get(key):
        frappe.throw("No OTP Sent or Expired.")

    stored_otp = frappe.cache().get(key).decode("utf-8")
    if not stored_otp == otp:
        frappe.throw("Incorrect OTP")
    try:
        user = frappe.db.get("User", email)
        frappe.cache().delete(key)
        return generate_key(user)
    except Exception as e:
        frappe.throw("User not found.")


def generate_key(user):
    user_details = frappe.get_doc("User", user)
    api_secret = api_key = ""
    if not user_details.api_key and not user_details.api_secret:
        api_secret = frappe.generate_hash(length=15)
        api_key = frappe.generate_hash(length=15)
        user_details.api_key = api_key
        user_details.api_secret = api_secret
        user_details.save(ignore_permissions=True)
        frappe.db.commit()
    else:
        api_secret = user_details.get_password("api_secret")
        api_key = user_details.get("api_key")
    return {"api_secret": api_secret, "api_key": api_key}
