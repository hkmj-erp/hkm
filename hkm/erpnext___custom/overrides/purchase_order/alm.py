from datetime import date
from frappe.model.document import Document
from frappe.model.workflow import get_workflow_name
from frappe.utils.data import get_url
from frappe.utils.verified_command import get_signed_params
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
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
        remove_all_assignments(doc)
        assign_purchase_order(doc, user)
        send_approval_email(doc, user)


    if current_state == "Final Level Approved":
        remove_all_assignments(doc)
    return

def assign_purchase_order(doc,user):
    todo_doc = frappe.get_doc(
        {
            "doctype": "ToDo",
            "status": "Open",
            "priority": "Medium",
            "allocated_to": user,
            "assigned_by": frappe.session.user,
            "reference_type": "Purchase Order",
            "reference_name": doc.name,
            "date": date.today(),
            "description": "Purchase Order approval for " + doc.supplier_name,
        }
    )
    todo_doc.insert()

def send_approval_email(doc, user):
    currency = frappe.get_cached_value("Company", doc.company, "default_currency")
    allowed_options = get_allowed_options(user,doc)
    template_data = {
        "doc": doc,
        "user": user,
        "currency": currency,
        "approval_link": get_approval_link(doc, user, allowed_options),
        "rejection_link": get_rejection_link(doc, user),
        "document_link": frappe.utils.get_url_to_form(doc.doctype, doc.name),
    }

    message = frappe.render_template(
        "hkm/erpnext___custom/overrides/purchase_order/approval_template.html",template_data
    )

    email_args = {
        "recipients": [user],
        "message": message,
        "subject": "#PO :{} Approval".format(
            doc.name
        ), 
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


def remove_all_assignments(doc):
    frappe.db.sql(
        """
		UPDATE `tabToDo`
		SET status = 'Closed'
		WHERE status = 'Open'
		AND reference_name = '{}'
		AND reference_type = 'Purchase Order'
		""".format(
            doc.name
        )
    )
    frappe.db.commit()
    return

def get_confirm_workflow_action_url(doc, action, user):
	confirm_action_method = (
		"/api/method/hkm.erpnext___custom.overrides.purchase_order.workflow_action.confirm_action"
	)

	params = {
		"action": action,
		"doctype": doc.get("doctype"),
		"docname": doc.get("name"),
		"user": user,
	}

	return get_url(confirm_action_method + "?" + get_signed_params(params))

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

def check_user_eligible(user,transition,doc):
	roles = frappe.get_roles(user)
	if transition['allowed'] in roles and ((transition['condition'] is None) or eval(transition['condition'].replace('frappe.session.user','user'))):
		return True
	return False
	#if wf_item is None user.has_role(System Manager)

def get_allowed_options(user:str,doc:Document):
	workflow = get_workflow_name(doc.get('doctype'))
	transitions = frappe.get_all('Workflow Transition', fields=['allowed', 'action', 'state', 'allow_self_approval', 'next_state', '`condition`'], filters=[['parent', '=', workflow],['state', '=', get_doc_workflow_state(doc)]])
	applicable_actions = []
	for transition in transitions:
		if check_user_eligible(user,transition,doc):
			applicable_actions.append(transition['action'])
	applicable_actions_unique = set(applicable_actions)
	return applicable_actions_unique


def get_workflow_action_url(action, doc, user):
	apply_action_method = "/api/method/hkm.erpnext___custom.po_approval.workflow_action.apply_action"

	params = {
		"doctype": doc.get('doctype'),
		"docname": doc.get('name'),
		"action": action,
		"current_state": get_doc_workflow_state(doc),
		"user": user,
		"last_modified": doc.get('modified')
	}

	return get_url(apply_action_method + "?" + get_signed_params(params))