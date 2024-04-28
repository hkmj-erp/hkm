from erpnext.buying.doctype.purchase_order.purchase_order import PurchaseOrder
import frappe, re
from hkm.erpnext___custom.extend.accounts_controller import validate_gst_entry
from hkm.erpnext___custom.overrides.buying_validations import (
    check_items_are_not_from_template,
    validate_work_order_item,
)
from hkm.erpnext___custom.po_approval.mail_template import message_str
from datetime import date
from frappe.utils.background_jobs import enqueue
from frappe.workflow.doctype.workflow_action.workflow_action import (
    get_doc_workflow_state,
)
# from hkm.erpnext___custom.po_approval.po_workflow_trigger import check_alm


class HKMPurchaseOrder(PurchaseOrder):
    def __init__(self, *args, **kwargs):
        super(HKMPurchaseOrder, self).__init__(*args, **kwargs)

    def before_save(self):
        # super().before_save() #Since there is no before_insert in parent
        validate_gst_entry(self)
        self.refresh_alm()

    def on_update(self):
        super().on_update()
        assign_and_notify_next_authority(self)
    
    def refresh_alm(self):
        if hasattr(self, "department") and self.department == "":
            frappe.throw("Department is not set.")
        alm = self.get_alm()
        if alm is not None:
            self.recommended_by = alm["recommender"]
            self.first_approving_authority = alm["first_approver"]
            self.final_approving_authority = alm["final_approver"]
        else:
            frappe.throw("ALM Levels are not set for this ALM Center in this document")
    
    def get_alm(self):
        final_alm_level = None
        alms = frappe.db.sql(
            """
                            select alm.name
                            from `tabALM` alm
                            where alm.document = '{}' and alm.company = '{}'
                            """.format(
                self.doctype, self.company
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
                    alm["name"], self.department
                ),
                as_dict=1,
            )
            if len(alm_levels) > 0:
                amount_field = "rounded_total"
                deciding_amount = getattr(self, amount_field)
                doc_expense_type = self.type
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

    def validate(self):
        super().validate()
        check_items_are_not_from_template(self)
        validate_work_order_item(self)
        self.update_extra_description_from_mrn()
        self.validate_mrn_availble()
        return

    def update_extra_description_from_mrn(self):
        descriptions = []
        mrns = frappe.db.get_all(
            "Purchase Order Item",
            pluck="material_request",
            filters={"parent": self.name},
        )
        mrns = set(mrns)
        for mrn in mrns:
            if mrn is not None:
                mrn_doc = frappe.get_doc("Material Request", mrn)
                if mrn_doc.description is not None:
                    descriptions.append(mrn_doc.purpose + "\n" + mrn_doc.description)
        description = ", ".join(descriptions)
        if self.extra_description == None or self.extra_description.strip() == "":
            self.extra_description = description
        return

    def validate_mrn_availble(self):
        for item in self.items:
            if item.material_request is None:
                frappe.throw(
                    f"Item {item.item_name} doesn't have a linked MRN. Seems this Purchase Order is not linked from any MRN."
                )
        return

    def before_insert(self):
        # super().before_insert() #Since there is no before_insert in parent
        self.set_naming_series()
        self.validate_work_request_status()

    def set_naming_series(self):
        if self.meta.get_field("for_a_work_order") and self.for_a_work_order:
            self.naming_series = "WOR-ORD-.YYYY.-"
        else:
            self.naming_series = "PUR-ORD-.YYYY.-"

    def validate_work_request_status(self):
        if not (self.meta.get_field("for_a_work_order") and self.for_a_work_order == 1):
            return
        mrns = []
        for row in self.get("items"):
            mrn = row.material_request
            if mrn is not None and mrn not in mrns:
                mrns.append(mrn)
        for mrn in mrns:
            mrn_doc = frappe.get_doc("Material Request", mrn)
            if mrn_doc.completed == 1:
                frappe.throw(
                    "<p> Work Order is not allowed in respect to this work request ({}) because it has been marked as <b class='text-danger'>COMPLETED</b> by the User (MRN Approver).</p>".format(
                        mrn_doc.name
                    )
                )
        return


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
