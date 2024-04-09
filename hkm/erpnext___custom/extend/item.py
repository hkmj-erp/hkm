import frappe
from frappe.utils.background_jobs import enqueue
from frappe.utils import time_diff_in_hours, time_diff_in_seconds, date_diff, flt
from frappe.model.workflow import apply_workflow

system_admin = "nrhd@hkm-group.org"


def validate(self, method):
    frappe.throw("Hare Krishna")

def item_creation_update(self, method):
    if self.get("item_creation_request"):  # self.flags.is_new_doc and
        ic_request = frappe.get_doc(
            "Item Creation Request", self.get("item_creation_request")
        )

        message = success_mail(self, ic_request)
        email_args = {
            "recipients": [ic_request.owner],
            "message": message,
            "subject": "Item {} Created".format(ic_request.item_name),
            # "attachments": [frappe.attach_print(doc.doctype, doc.name, file_name=doc.name)],
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

        apply_workflow(ic_request, "Confirm as Done")
        frappe.errprint("Doing Creation")
        frappe.db.commit()
    frappe.errprint("Doing 2222")
    return


def success_mail(item, ic_request):
    time_taken, postfix = (
        time_diff_in_hours(item.creation, ic_request.creation),
        "hours",
    )
    if time_taken < 1:
        time_taken, postfix = (
            time_diff_in_seconds(item.creation, ic_request.creation) / 60,
            "minutes",
        )
    elif time_taken > 23:
        time_taken, postfix = date_diff(item.creation, ic_request.creation), "days"
    time_taken = flt(time_taken, 2)
    message = """
				<p>Hare Krishna,</p>
				<p>We have created an ITEM Code as requested by you. Please check the details.</p>
				<p>&nbsp;</p>
				<p><strong>Item Name : {}</strong></p>
				<p><strong>Item Code : {}</strong></p>
				<p><strong>Link to Item for more details : {}</strong></p>
				<p>&nbsp;</p>
				<p><em>We have created this within <strong>{} {}</strong>, you raised the request.</em></p>
				Please contact <strong>{}</strong> for any issues.
				<p>&nbsp;</p>
				<p>Thanks,</p>
				<p>ERP Team</p>
				""".format(
        item.item_name,
        item.item_code,
        frappe.utils.get_url_to_form("Item", item.name),
        time_taken,
        postfix,
        item.owner,
    )
    return message


@frappe.whitelist()
def fetch_item_code(item_group):
    if frappe.db.exists("Item Group", item_group):
        item_grp_doc = frappe.get_doc("Item Group", item_group)
        series = item_grp_doc.get("item_code_series")
        if series is not None and series.strip() != "":
            codes = frappe.db.sql(
                """
						select CAST(TRIM(LEADING '{}-' FROM item_code ) AS int) AS new_code 
						from `tabItem`
						where item_code LIKE '{}-%'
						order by new_code DESC
							""".format(
                    series, series
                ),
                as_dict=1,
            )

            last_code = codes[0]["new_code"] if len(codes) > 0 else 1
            last_code = str(last_code + 1).zfill(4)
            return series + "-" + last_code
    return 0


def item_taxes_and_income_account_set(self, method):
    if self.get("item_creation_request"):
        ic_request = frappe.get_doc(
            "Item Creation Request", self.get("item_creation_request")
        )
        if ic_request.is_sales_item:
            tax = ic_request.tax_category
            if not (tax is None or tax == ""):
                self.append(
                    "taxes",
                    {
                        "item_tax_template": tax,
                    },
                )
            if ic_request.default_company:
                self.append(
                    "item_defaults",
                    {
                        "company": ic_request.default_company,
                        "income_account": ic_request.default_sales_income_account,
                    },
                )


def update_item_code_in_barcodes(self, method):
    self.append(
        "barcodes",
        frappe._dict(
            {
                "barcode": self.item_code,
            }
        ),
    )
