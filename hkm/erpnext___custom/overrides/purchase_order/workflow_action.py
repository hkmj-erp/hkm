import frappe
from frappe.model.document import Document
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_confirm_workflow_action_url,
    get_doc_workflow_state,
    return_action_confirmation_page,
)
from frappe.model.workflow import apply_workflow
from frappe.utils.verified_command import verify_request
from frappe.utils import get_datetime


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
