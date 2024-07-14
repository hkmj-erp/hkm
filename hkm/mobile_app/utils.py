import json
from mimetypes import guess_type
from random import randint
import frappe
from frappe.utils.image import optimize_image
from frappe.core.api.file import create_new_folder


@frappe.whitelist()
def attach_image_to_doc():
    data = json.loads(frappe.form_dict.data)

    docfield = data["field"]

    folder = data["folder"]

    if not folder_exists(folder):
        folder_name_parts = folder.split("/")
        create_new_folder(folder_name_parts[1], folder_name_parts[0])

    doc = frappe.get_doc(data["doctype"], data["name"])

    if doc.get(docfield):
        images = frappe.get_all(
            "File",
            filters={"attached_to_name": data["name"], "attached_to_field": docfield},
            pluck="name",
        )
        if len(images) > 0:
            frappe.delete_doc("File", images[0], ignore_permissions=True)
            frappe.db.commit()

    files = frappe.request.files

    if "image" in files:
        file = files["image"]
        content = file.stream.read()
        fileref = file.filename

        content_type = guess_type(fileref)[0]
        if content_type.startswith("image/"):
            args = {"content": content, "content_type": content_type}
            args["max_width"] = 1200
            content = optimize_image(**args)

        filename = (
            doc.name
            + "-"
            + f"profile"
            + str(randint(100, 999))
            + "."
            + fileref.split(".")[-1]
        )
        frappe.local.uploaded_file = content
        frappe.local.uploaded_filename = filename

        image_doc = frappe.get_doc(
            {
                "doctype": "File",
                "attached_to_doctype": doc.doctype,
                "attached_to_name": doc.name,
                "attached_to_field": docfield,
                "folder": folder,
                "file_name": filename,
                "is_private": 0,
                "content": content,
            }
        ).save(ignore_permissions=1)
        frappe.db.commit()
        doc.set(docfield, image_doc.file_url)
    doc.reload()
    doc.save()


def folder_exists(folder_path):
    folder_name_parts = folder_path.split("/")
    if len(folder_name_parts) == 0:
        return True

    folder_name = folder_name_parts[1]
    folders = frappe.get_all("File", filters={"is_folder": 1, "file_name": folder_name})
    if len(folders) > 0:
        return True
    else:
        return False
