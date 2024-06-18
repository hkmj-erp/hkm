from datetime import date
from hkm.erpnext___custom.overrides.purchase_order.whatsapp import (
    send_whatsapp_approval,
)
from frappe.model.document import Document
from frappe.model.workflow import get_workflow_name
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
)
from hkm.erpnext___custom.overrides.purchase_order.workflow_action import (
    get_approval_link,
    get_rejection_link,
)
import frappe
from frappe.utils.background_jobs import enqueue


def get_alm_level(doc):
    """
    Get ALM level for purchase order.
    """
    amount_field = "rounded_total"
    deciding_amount = getattr(doc, amount_field)

    for l in frappe.db.sql(
        f"""
                SELECT level.*
                FROM `tabALM` alm
                JOIN `tabALM Level` level
                    ON level.parent = alm.name
                WHERE alm.document = "{doc.doctype}"
                    AND alm.company = "{doc.company}"
                    AND level.department = "{doc.department}"
                    AND (level.expense_type = "ANY" OR level.expense_type = "{doc.type}")    
                ORDER BY level.idx
                    """,
        as_dict=1,
    ):
        if eval(f"{deciding_amount} {l.amount_condition}"):
            return l
    return None


def assign_and_notify_next_authority(doc):
    user = None
    current_state = doc.workflow_state
    states = ("Checked", "Recommended", "First Level Approved")
    approvers = (
        "recommended_by",
        "first_approving_authority",
        "final_approving_authority",
    )
    if current_state in states:
        for i, state in enumerate(states):
            if current_state == state:
                for approver in approvers[i : len(approvers)]:
                    if (
                        getattr(doc, approver) is not None
                        and getattr(doc, approver) != ""
                    ):
                        user = getattr(doc, approver)
                        break
                break
        if user is None:
            frappe.throw("Next authority is not Found. Please check ALM.")
        close_assignments(doc)
        assign_to_next_approving_authority(doc, user)
        po_approval_settings = frappe.get_cached_doc("HKM General Settings")
        mobile_no = frappe.get_value("User", user, "mobile_no")
        if po_approval_settings.po_approval_on_whatsapp and mobile_no:
            allowed_options = get_allowed_options(user, doc)
            send_whatsapp_approval(doc, user, mobile_no, allowed_options)
        else:
            send_email_approval(doc, user)

    if current_state == "Final Level Approved":
        close_assignments(doc, remove=True)
    frappe.db.commit()
    return


def assign_to_next_approving_authority(doc, user):
    todo_doc = frappe.get_doc(
        {
            "doctype": "ToDo",
            "status": "Open",
            "allocated_to": user,
            "assigned_by": frappe.session.user,
            "reference_type": doc.doctype,
            "reference_name": doc.name,
            "date": date.today(),
            "description": "Purchase Order approval for " + doc.supplier_name,
        }
    )
    todo_doc.insert()
    return


def send_email_approval(doc, user):
    currency = frappe.get_cached_value("Company", doc.company, "default_currency")
    allowed_options = get_allowed_options(user, doc)
    template_data = {
        "doc": doc,
        "user": user,
        "currency": currency,
        "approval_link": get_approval_link(doc, user, allowed_options),
        "rejection_link": get_rejection_link(doc, user),
        "document_link": frappe.utils.get_url_to_form(doc.doctype, doc.name),
    }

    email_args = {
        "recipients": [user],
        "message": frappe.render_template(
            "hkm/erpnext___custom/overrides/purchase_order/templates/email_template.html",
            template_data,
        ),
        "subject": "#PO :{} Approval".format(doc.name),
        "reference_doctype": doc.doctype,
        "reference_name": doc.name,
        "reply_to": doc.owner,
        "delayed": False,
        "sender": doc.owner,
    }
    enqueue(
        method=frappe.sendmail, queue="short", timeout=300, is_async=True, **email_args
    )
    return


def close_assignments(doc, remove=True):
    if remove:
        frappe.db.delete(
            "ToDo", {"reference_type": "Purchase Order", "reference_name": doc.name}
        )
    else:
        frappe.db.set_value(
            "ToDo",
            {"reference_type": "Purchase Order", "reference_name": doc.name},
            "status",
            "Closed",
        )
    return


def get_allowed_options(user: str, doc: Document):
    roles = frappe.get_roles(user)
    workflow = get_workflow_name(doc.get("doctype"))
    transitions = frappe.get_all(
        "Workflow Transition",
        fields=[
            "allowed",
            "action",
            "`condition`",
        ],
        filters=[
            ["parent", "=", workflow],
            ["state", "=", get_doc_workflow_state(doc)],
        ],
    )
    applicable_actions = []
    for transition in transitions:
        if transition["allowed"] in roles and (
            (transition["condition"] is None)
            or eval(transition["condition"].replace("frappe.session.user", "user"))
        ):
            applicable_actions.append(transition["action"])
    return set(applicable_actions)  ## Unique Actions
