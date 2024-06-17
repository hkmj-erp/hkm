import frappe, requests, json
from frappe.utils import cstr
from frappe.utils import getdate


def send_message():
    settings = frappe.get_cached_doc("WhatsApp Settings")
    url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"

    site_name = cstr(frappe.local.site)

    # qr_link = f"""https://{site_name}/api/method/prasadam_flow.pf_manage.doctype.pf_coupon_issue.pf_coupon_issue.get_coupon_qr?id=1213231232144122"""

    qr_link = "https://img.freepik.com/premium-vector/document-approval-concept_118813-7683.jpg"

    cleaned_mobile = "7357010770"

    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"+91{cleaned_mobile}",
            "type": "template",
            "template": {
                "name": "purchase_order_approval",
                "language": {"code": "en"},
                "components": [
                    {
                        "type": "header",
                        "parameters": [{"type": "image", "image": {"link": qr_link}}],
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": "KA Kitchen - TSFJ"},
                            {"type": "text", "text": "PUR-ORD-2024-02797"},
                            {"type": "text", "text": "Rajesh Kumar Khateek"},
                            {"type": "text", "text": "Checked"},
                            {"type": "text", "text": "₹ 2,268"},
                        ],
                    },
                    {
                        "type": "button",
                        "index": "0",
                        "sub_type": "url",
                        "parameters": [
                            {"type": "text", "text": "1qwd321we3d32"},
                        ],
                    },
                    {
                        "type": "button",
                        "index": "1",
                        "sub_type": "url",
                        "parameters": [
                            {"type": "text", "text": "1qwd321we3d32"},
                        ],
                    },
                ],
            },
        }
    )
    headers = {
        "Content-Type": "application/json",
        "Authorization": f'Bearer {settings.get_password("token")}',
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
