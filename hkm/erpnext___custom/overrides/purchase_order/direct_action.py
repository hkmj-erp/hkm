import frappe, imgkit
from frappe.utils.data import get_url
from frappe.utils.pdf import get_pdf
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
)
from hkm.erpnext___custom.overrides.purchase_order.workflow_action import (
    return_already_approved_page,
    return_success_page,
)
from frappe.utils.verified_command import get_signed_params, verify_request
from frappe.model.workflow import get_workflow_name, apply_workflow

from hkm.erpnext___custom.overrides.purchase_order.alm import get_allowed_options


# @frappe.whitelist(allow_guest=True)
# def get_purchase_order_details(po):
#     docs = frappe.get_all("Purchase Order", fields=["*"], filters={"name": po})
#     if not docs:
#         frappe.throw("Doesn't exist.")
#     doc = frappe._dict(docs[0])
#     items = frappe.get_all(
#         "Purchase Order Item",
#         fields=["*"],
#         filters={"parent": doc.name},
#         order_by="idx asc",
#     )
#     currency = frappe.get_cached_value("Company", doc.company, "default_currency")
#     print("Purchase Order Details")
#     print(doc.name)
#     print(doc.doctype)
#     template_data = {
#         "doc": doc,
#         "currency": currency,
#         "items": items,
#         "document_link": frappe.utils.get_url_to_form("Purchase Order", doc.name),
#     }
#     message_html = frappe.render_template(
#         "hkm/erpnext___custom/overrides/purchase_order/whatsapp_template.html",
#         template_data,
#     )
#     frappe.local.response.filename = f"approval_{doc.name}.pdf"
#     frappe.local.response.filecontent = get_pdf(message_html)
#     frappe.local.response.type = "download"


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
        "hkm/erpnext___custom/overrides/purchase_order/whatsapp_template.html",
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


def send_whatsapp_approval(doc, user):
    allowed_options = get_allowed_options(user, doc)
    approval_link = get_approval_link(doc, user, allowed_options)
    rejection_link = get_rejection_link(doc, user)
    # get_purchase_order_image

    ## send above generated image as a link to whatsapp give me link for that
    ## print image as link  and then send that as a message


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
    confirm_action_method = (
        "/api/method/hkm.erpnext___custom.po_approval.workflow_action.confirm_action"
    )

    params = {
        "action": action,
        "doctype": doc.get("doctype"),
        "docname": doc.get("name"),
        "user": user,
    }

    return get_url(confirm_action_method + "?" + get_signed_params(params))


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
