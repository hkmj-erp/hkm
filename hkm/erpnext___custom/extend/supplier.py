import frappe
from frappe.contacts.doctype.address.address import get_address_display
from frappe.utils import time_diff_in_hours, time_diff_in_seconds, date_diff, flt
from frappe.model.workflow import apply_workflow
from frappe.utils.background_jobs import enqueue
from frappe import _

system_admin = "nrhd@hkmjaipur.org"


def update_data_from_supplier_creation_request(self, method):
    if self.flags.is_new_doc and self.get("supplier_creation_request"):
        creation_doc = frappe.get_doc(
            "Supplier Creation Request", self.get("supplier_creation_request")
        )
        fetch_address_from_creation_request(self, creation_doc)
        fetch_bank_account_from_creation_request(self, creation_doc)
        frappe.db.commit()

        # Notify Requestor

        message = success_mail(self, creation_doc)
        email_args = {
            "recipients": [creation_doc.owner],
            "message": message,
            "subject": "Item {} Created".format(creation_doc.supplier_name),
            "reference_doctype": self.doctype,
            "reference_name": self.name,
            "reply_to": self.owner if self.owner != "Administrator" else system_admin,
            "delayed": False,
            "sender": self.owner,
        }
        enqueue(
            method=frappe.sendmail,
            queue="short",
            timeout=300,
            is_async=True,
            **email_args
        )

        apply_workflow(creation_doc, "Confirm as Done")


def fetch_bank_account_from_creation_request(self, creation_doc):
    if creation_doc.bank:
        bank_account = frappe.get_doc(
            {
                "doctype": "Bank Account",
                "bank": creation_doc.bank,
                "account_name": creation_doc.bank_account_name,
                "party_type": "Supplier",
                "party": self.name,
                "branch_code": creation_doc.bank_branch_code,
                "bank_account_no": creation_doc.bank_account_number,
            }
        ).insert(ignore_links=True)
    return


def fetch_address_from_creation_request(self, creation_doc):
    if creation_doc.gstin:
        self.gst_category = "Registered Regular"
    elif self.country != "India":
        self.gst_category = "Overseas"
    else:
        self.gst_category = "Unregistered"

    address = make_address(creation_doc)
    address_display = get_address_display(address.name)

    self.db_set("supplier_primary_address", address.name)
    self.db_set("primary_address", address_display)
    return


def make_address(creation_doc):
    reqd_fields = []
    for field in ["city", "country"]:
        if not creation_doc.get(field):
            reqd_fields.append("<li>" + field.title() + "</li>")

    if reqd_fields:
        msg = _("Following fields are mandatory to create address:")
        frappe.throw(
            "{0} <br><br> <ul>{1}</ul>".format(msg, "\n".join(reqd_fields)),
            title=_("Missing Values Required"),
        )

    address = frappe.get_doc(
        {
            "doctype": "Address",
            "address_title": creation_doc.get("name"),
            "address_line1": creation_doc.get("address_line_1"),
            "address_line2": creation_doc.get("address_line_2"),
            "city": creation_doc.get("city"),
            "state": creation_doc.get("state"),
            "pincode": creation_doc.get("pincode"),
            "country": creation_doc.get("country"),
            "gst_category": creation_doc.get("gst_category"),
            "gstin": creation_doc.get("gstin"),
            "phone": creation_doc.get("mobile_number"),
            "links": [
                {
                    "link_doctype": creation_doc.get("doctype"),
                    "link_name": creation_doc.get("name"),
                }
            ],
        }
    ).insert()

    return address


def success_mail(supplier, sc_request):
    time_taken, postfix = (
        time_diff_in_hours(supplier.creation, sc_request.creation),
        "hours",
    )
    if time_taken < 1:
        time_taken, postfix = (
            time_diff_in_seconds(supplier.creation, sc_request.creation) / 60,
            "minutes",
        )
    elif time_taken > 23:
        time_taken, postfix = date_diff(supplier.creation, sc_request.creation), "days"
    time_taken = flt(time_taken, 2)
    message = """
				<p>Hare Krishna,</p>
				<p>We have created an Supplier as requested by you. Please check the details.</p>
				<p>&nbsp;</p>
				<p><strong>Supplier Name : {}</strong></p>
				<p><strong>Link to Supplier for more details : {}</strong></p>
				<p>&nbsp;</p>
				<p><em>We have created this within <strong>{} {}</strong>, you raised the request.</em></p>
				Please contact <strong>{}</strong> for any issues.
				<p>&nbsp;</p>
				<p>Thanks,</p>
				<p>ERP Team</p>
				""".format(
        supplier.supplier_name,
        frappe.utils.get_url_to_form("Supplier", supplier.name),
        time_taken,
        postfix,
        supplier.owner,
    )
    return message


item_supplier_admin = "Item Manager"


def creation_from_gstin(self, method):
    if (
        self.is_new()
        and not self.get("gstin")
        and not item_supplier_admin in frappe.get_roles(frappe.session.user)
    ):
        frappe.throw(
            "You are not allowed to create a Supplier without GSTIN. Raise through Supplier Creation Request."
        )
    return
