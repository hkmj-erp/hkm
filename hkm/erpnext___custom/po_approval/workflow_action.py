from hkm.erpnext___custom.doctype.hkm_debug.hkm_debug import add_debug_entry
import frappe
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_next_possible_transitions,
    get_doc_workflow_state,
)
from frappe.model.workflow import get_workflow_name, apply_workflow
from frappe.utils.verified_command import get_signed_params, verify_request
from frappe.utils import get_url, get_datetime


def check_user_eligible(user, transition, doc):
    roles = frappe.get_roles(user)
    if transition["allowed"] in roles and (
        (transition["condition"] is None)
        or eval(transition["condition"].replace("frappe.session.user", "user"))
    ):
        return True
    return False
    # if wf_item is None user.has_role(System Manager)


def get_allowed_options(user, doc):
    workflow = get_workflow_name(doc.get("doctype"))
    transitions = frappe.get_all(
        "Workflow Transition",
        fields=[
            "allowed",
            "action",
            "state",
            "allow_self_approval",
            "next_state",
            "`condition`",
        ],
        filters=[
            ["parent", "=", workflow],
            ["state", "=", get_doc_workflow_state(doc)],
        ],
    )
    applicable_actions = []
    for transition in transitions:
        if check_user_eligible(user, transition, doc):
            applicable_actions.append(transition["action"])
    applicable_actions_unique = set(applicable_actions)
    return applicable_actions_unique


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


def get_workflow_action_url(action, doc, user):
    apply_action_method = (
        "/api/method/hkm.erpnext___custom.po_approval.workflow_action.apply_action"
    )

    params = {
        "doctype": doc.get("doctype"),
        "docname": doc.get("name"),
        "action": action,
        "current_state": get_doc_workflow_state(doc),
        "user": user,
        "last_modified": doc.get("modified"),
    }

    return get_url(apply_action_method + "?" + get_signed_params(params))


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
        debug_data = f"(Before) User : {frappe.session.user} | State: {workflow_state} | Action: {action}"
        newdoc = apply_workflow(doc, action)
        debug_data = f"{debug_data}\n(After) User : {frappe.session.user} | State: {newdoc.workflow_state}"
        add_debug_entry(
            doctype=doc.doctype,
            data=debug_data,
            name=doc.name,
            ip=frappe.local.request_ip,
        )
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


def return_action_confirmation_page(doc, action, action_link, alert_doc_change=False):
    template_params = {
        "title": doc.get("name"),
        "doctype": doc.get("doctype"),
        "docname": doc.get("name"),
        "action": action,
        "action_link": action_link,
        "alert_doc_change": alert_doc_change,
    }

    template_params["doc_link"] = frappe.utils.get_url_to_form(doc.doctype, doc.name)

    frappe.respond_as_web_page(
        title=None,
        html=None,
        indicator_color="blue",
        template="po_workflow_action",
        context=template_params,
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
