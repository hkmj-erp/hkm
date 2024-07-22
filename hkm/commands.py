import json
import click

import frappe


relevant_sites = [
    # "hkmjerp.in",
    # "erp.hkmkota.org",
    # "erp.hkmjodhpur.org",
    # "erp.hkmudaipur.org",
    # "vcmerp.in",
    # "lko.vcmerp.in",
    # "erp.hkmmumbai.com",
    "erp.harekrishnamandir.org",
]


@click.command("operation")
@click.argument("method")
def operation(method):
    for site in relevant_sites:
        ret = ""
        print(f"Site : {site}")
        try:
            frappe.init(site=site)
            frappe.connect(site=site)
            ret = frappe.get_attr(method)
            ret()
            if frappe.db:
                frappe.db.commit()
        finally:
            frappe.destroy()

        if ret:
            from frappe.utils.response import json_handler

            print(json.dumps(ret, default=json_handler))


commands = [operation]
