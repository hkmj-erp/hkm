import frappe, re
from datetime import date
from frappe.utils.background_jobs import enqueue
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
)

from hkm.erpnext___custom.po_approval.mail_template import message_str


def check_alm(self, method=None):
    if hasattr(self, "department") and self.department == "":
        frappe.throw("Department is not set.")
    update_alm_data(self)
    assign_and_notify_next_authority(self)
    return


def update_alm_data(doc):
    alm = get_alm(doc)
    if alm is not None:
        frappe.db.set_value(
            "Purchase Order", doc.name, "recommended_by", alm["recommender"]
        )
        frappe.db.set_value(
            "Purchase Order",
            doc.name,
            "first_approving_authority",
            alm["first_approver"],
        )
        frappe.db.set_value(
            "Purchase Order",
            doc.name,
            "final_approving_authority",
            alm["final_approver"],
        )
        frappe.db.commit()
        return

    else:
        frappe.throw("ALM Levels are not set for this ALM Center in this document")


def get_alm(doc):
    final_alm_level = None
    alms = frappe.db.sql(
        """
						select alm.name
						from `tabALM` alm
						where alm.document = '{}' and alm.company = '{}'
						""".format(
            doc.doctype, doc.company
        ),
        as_dict=1,
    )
    if len(alms) != 0:
        alm = alms[0]
        alm_levels = frappe.db.sql(
            """
						select *
						from `tabALM Level` alml
						where alml.parent = '{}' and alml.department = '{}'
                        order by alml.idx
						""".format(
                alm["name"], doc.department
            ),
            as_dict=1,
        )
        if len(alm_levels) > 0:
            # if alm['amount_field'] == "" or alm['amount_field'] is None:
            # 	frappe.throw("Amount Field for comparsion is not set in ALM.")
            amount_field = "rounded_total"
            deciding_amount = getattr(doc, amount_field)
            doc_expense_type = doc.type
            for level in alm_levels:
                if level["expense_type"] == "ANY":
                    if eval(str(deciding_amount) + level["amount_condition"]):
                        final_alm_level = level
                        break
                else:
                    if (
                        eval(str(deciding_amount) + level["amount_condition"])
                        and doc_expense_type == level["expense_type"]
                    ):
                        final_alm_level = level
                        break

    return final_alm_level


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
        assign(doc, user)

    if current_state == "Final Level Approved":
        remove_all_assignments(doc)
    # frappe.db.commit()
    return


def assign(doc, user):
    remove_all_assignments(doc)

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

    message = message_str(doc, user)

    email_args = {
        "recipients": [user],
        "message": message,
        "subject": "#PO :{} Approval".format(
            doc.name
        ),  # .format(self.start_date, self.end_date),
        # "attachments": [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name)],
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
