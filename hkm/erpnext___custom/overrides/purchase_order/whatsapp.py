from frappe.utils.data import get_url
from hkm.erpnext___custom.overrides.purchase_order.workflow_action import (
    return_already_approved_page,
)
import frappe, requests, json, imgkit
from frappe.model.document import Document
from frappe.model.workflow import apply_workflow
from frappe.utils import cstr
from frappe.utils.verified_command import get_signed_params, verify_request
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
    return_success_page,
)


def send_whatsapp_approval(doc, user, mobile_no, allowed_options):
    approval_link = get_approval_link(doc, user, allowed_options)
    rejection_link = get_rejection_link(doc, user)
    send_whatsapp(doc, mobile_no, approval_link, rejection_link)


def get_short_link_name(long_link):
    doc = frappe.get_doc(
        {"doctype": "HKM Redirect", "redirect_to": long_link, "ephemeral": 1}
    )
    doc.insert(ignore_permissions=True)
    return doc.name


def send_whatsapp(
    doc: Document, mobile_no: str, approval_link: str, rejection_link: str
):
    approval_link_name = get_short_link_name(approval_link)
    rejection_link_name = get_short_link_name(rejection_link)

    settings = frappe.get_cached_doc("WhatsApp Settings")
    po_approval_settings = frappe.get_cached_doc("HKM General Settings")
    url = f"{settings.url}/{settings.version}/{settings.phone_id}/messages"

    site_name = cstr(frappe.local.site)

    po_image_link = f"https://{site_name}/api/method/hkm.erpnext___custom.overrides.purchase_order.whatsapp.get_purchase_order_image?docname={doc.name}"

    cleaned_mobile = mobile_no

    payload = json.dumps(
        {
            "messaging_product": "whatsapp",
            "recipient_type": "individual",
            "to": f"+91{cleaned_mobile}",
            "type": "template",
            "template": {
                "name": po_approval_settings.po_whatsapp_template,
                "language": {"code": "en"},
                "components": [
                    {
                        "type": "header",
                        "parameters": [
                            {"type": "image", "image": {"link": po_image_link}}
                        ],
                    },
                    {
                        "type": "body",
                        "parameters": [
                            {"type": "text", "text": doc.department},
                            {"type": "text", "text": doc.name},
                            {"type": "text", "text": doc.supplier_name},
                            {"type": "text", "text": doc.workflow_state},
                            {
                                "type": "text",
                                "text": doc.get_formatted(
                                    "grand_total", absolute_value=True
                                ),
                            },
                        ],
                    },
                    {
                        "type": "button",
                        "index": "0",
                        "sub_type": "url",
                        "parameters": [
                            {"type": "text", "text": approval_link_name},
                        ],
                    },
                    {
                        "type": "button",
                        "index": "1",
                        "sub_type": "url",
                        "parameters": [
                            {"type": "text", "text": rejection_link_name},
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


def get_approval_link(doc, user, allowed_options):
    if "Recommend" in allowed_options:
        return get_confirm_workflow_action_url(doc, "Recommend", user)
    if "First Approve" in allowed_options:
        return get_confirm_workflow_action_url(doc, "First Approve", user)
    if "Final Approve" in allowed_options:
        return get_confirm_workflow_action_url(doc, "Final Approve", user)
    else:
        frappe.throw(
            "Next ALM User is not allowed to approve the Document. Please ask for permission."
        )


def get_rejection_link(doc, user):
    return get_confirm_workflow_action_url(doc, "Reject", user)


def get_confirm_workflow_action_url(doc, action, user):
    confirm_action_method = "/api/method/hkm.erpnext___custom.overrides.purchase_order.whatsapp.confirm_action"

    params = {
        "action": action,
        "doctype": doc.get("doctype"),
        "docname": doc.get("name"),
        "user": user,
    }

    return get_url(confirm_action_method + "?" + get_signed_params(params))


@frappe.whitelist(allow_guest=True)
def get_purchase_order_image(docname):
    docs = frappe.get_all("Purchase Order", fields=["*"], filters={"name": docname})
    if not docs:
        frappe.throw("Doesn't exist.")
    doc = frappe._dict(docs[0])
    items = frappe.get_all(
        "Purchase Order Item",
        fields=["*"],
        filters={"parent": doc.name},
        order_by="idx asc",
    )
    currency = frappe.get_cached_value("Company", doc.company, "default_currency")
    template_data = {
        "doc": doc,
        "currency": currency,
        "items": items,
        "document_link": frappe.utils.get_url_to_form("Purchase Order", doc.name),
    }
    message_html = frappe.render_template(
        "hkm/erpnext___custom/overrides/purchase_order/templates/whatsapp_template.html",
        template_data,
    )
    img = imgkit.from_string(
        message_html,
        False,
        options={
            "format": "png",
        },
    )

    frappe.local.response.filename = f"approval_{doc.name}.png"
    frappe.local.response.filecontent = img
    frappe.local.response.type = "download"


@frappe.whitelist(allow_guest=True)
def confirm_action(doctype, docname, user, action):
    if not verify_request():
        return

    logged_in_user = frappe.session.user
    if logged_in_user == "Guest" and user:
        # to allow user to apply action without login
        frappe.set_user(user)

    doc = frappe.get_doc(doctype, docname)

    ### Additional by NRHD
    workflow_state = get_doc_workflow_state(doc)
    if (
        (workflow_state == "Final Level Approved" and action == "Final Approve")
        or (workflow_state == "First Level Approved" and action == "First Approve")
        or (workflow_state == "Recommended" and action == "Recommend")
    ):
        return_already_approved_page(doc)
    ###
    else:
        newdoc = apply_workflow(doc, action)
        frappe.db.commit()
        return_success_page(newdoc)

    # reset session user
    if logged_in_user == "Guest":
        frappe.set_user(logged_in_user)
