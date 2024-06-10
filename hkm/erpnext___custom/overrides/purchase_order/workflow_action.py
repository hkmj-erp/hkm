from frappe.model.document import Document
from frappe.utils.data import get_url
from hkm.erpnext___custom.doctype.hkm_debug.hkm_debug import add_debug_entry
import frappe
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_confirm_workflow_action_url,
    get_doc_workflow_state,
    return_action_confirmation_page,
)
from frappe.model.workflow import apply_workflow, get_workflow_name
from frappe.utils.verified_command import get_signed_params, verify_request
from frappe.utils import get_datetime


def get_workflow_action_url(action, doc, user):
    apply_action_method = "/api/method/hkm.erpnext___custom.overrides.purchase_order.workflow_action.apply_action"

    params = {
        "doctype": doc.get("doctype"),
        "docname": doc.get("name"),
        "action": action,
        "current_state": get_doc_workflow_state(doc),
        "user": user,
        "last_modified": doc.get("modified"),
    }

    return get_url(apply_action_method + "?" + get_signed_params(params))


@frappe.whitelist(allow_guest=True)
def apply_action(
    action, doctype, docname, current_state, user=None, last_modified=None
):
    if not verify_request():
        return

    doc = frappe.get_doc(doctype, docname)
    doc_workflow_state = get_doc_workflow_state(doc)

    if doc_workflow_state == current_state:
        action_link = get_confirm_workflow_action_url(doc, action, user)

        if not last_modified or get_datetime(doc.modified) == get_datetime(
            last_modified
        ):
            return_action_confirmation_page(doc, action, action_link)
        else:
            return_action_confirmation_page(
                doc, action, action_link, alert_doc_change=True
            )

    else:
        return_link_expired_page(doc, doc_workflow_state)


def return_success_page(doc):
    frappe.respond_as_web_page(
        ("Success"),
        ("{0}: {1} is set to state {2}").format(
            doc.get("doctype"),
            frappe.bold(doc.get("name")),
            frappe.bold(get_doc_workflow_state(doc)),
        ),
        indicator_color="green",
    )


def return_already_approved_page(doc):
    frappe.respond_as_web_page(
        ("Already Approved"),
        ("The doument ( {0} ) is already {1}.").format(
            frappe.bold(doc.get("name")), frappe.bold(get_doc_workflow_state(doc))
        ),
        indicator_color="yellow",
    )


def return_link_expired_page(doc, doc_workflow_state):
    frappe.respond_as_web_page(
        ("Link Expired"),
        ("Document {0} has been set to state {1} by {2}").format(
            frappe.bold(doc.get("name")),
            frappe.bold(doc_workflow_state),
            frappe.bold(frappe.get_value("User", doc.get("modified_by"), "full_name")),
        ),
        indicator_color="blue",
    )


def get_approval_link(doc, user, allowed_options):
    if "Recommend" in allowed_options:
        return get_workflow_action_url(action="Recommend", doc=doc, user=user)
    if "First Approve" in allowed_options:
        return get_workflow_action_url(action="First Approve", doc=doc, user=user)
    if "Final Approve" in allowed_options:
        return get_workflow_action_url(action="Final Approve", doc=doc, user=user)
    else:
        frappe.throw(
            "Next ALM User is not allowed to approve the Document. Please ask for permission."
        )


def get_rejection_link(doc, user):
    return get_workflow_action_url("Reject", doc, user)
