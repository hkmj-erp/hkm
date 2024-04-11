from hkm.mobile_app.test import TEST_EMAIL, TEST_OTP
from frappe.core.doctype.sms_settings.sms_settings import send_sms
import frappe, re
import random
import string

REDIS_PREFIX = "otp"


def random_string_generator(str_size, allowed_chars):
    return "".join(random.choice(allowed_chars) for x in range(str_size))


@frappe.whitelist(allow_guest=True)
def generate_otp(mobile=None, email=None, signature= None):
    if mobile:
        mobile = re.sub(r"\D", "", mobile)[-10:]
        if not frappe.db.exists("User", {"mobile_no": mobile}):
            frappe.throw("No User exists with this Mobile Number")
        user = frappe.get_doc("User", {"mobile_no": mobile})
        email = user.email
    else:
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
        if email == TEST_EMAIL:
            otp = TEST_OTP
        else:
            otp = random_string_generator(6, string.digits)
        frappe.cache().set(key, otp, ex=600)
    send_otp_on_email(email, otp)
    if phone:
        ## Send WhatsApp
        # parameters = [
        #     {"type": "text", "text": otp},
        #     {"type": "text", "text": "Dhananjaya"},
        # ]
        # resp = send_whatsapp_using_template(
        #     phone, "mobile_app_authentication", parameters
        # )

        ## Send SMS
        # message = f"Hare Krishna Dear {user.full_name}, Your OTP for login is {otp}."
        message = f"""Your app code is: {otp} \n-Hare Krishna Movement \nApp Hash: {signature}"""
        send_sms(receiver_list=[phone], msg=message)

    return


def send_otp_on_email(email, otp):
    frappe.sendmail(
        recipients=email,
        subject=f"OTP for Login into Mobile App!",
        message=f"Hare Krishna,<br>Please use the OTP below to login.<br><br><h4>{otp}</h4></a>",
        delayed=False,
    )


@frappe.whitelist(allow_guest=True)
def verify_otp(otp, email=None, mobile=None):
    user = None
    if mobile:
        mobile = re.sub(r"\D", "", mobile)[-10:]
        if not frappe.db.exists("User", {"mobile_no": mobile}):
            frappe.throw("No User exists with this Mobile Number")
        user = frappe.get_doc("User", {"mobile_no": mobile})
        email = user.name

    stored_otp = None
    if email == TEST_EMAIL:
        stored_otp = TEST_OTP
    else:
        key = f"{REDIS_PREFIX}:{email}"
        if not frappe.cache().get(key):
            frappe.throw("No OTP Sent or Expired.")

        stored_otp = frappe.cache().get(key).decode("utf-8")

    if not stored_otp == otp:
        frappe.throw("Incorrect OTP")
    try:
        if user is None:
            user = frappe.db.get("User", email)
        if email != TEST_EMAIL:
            frappe.cache().delete(key)
        return generate_key(user.name)
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
