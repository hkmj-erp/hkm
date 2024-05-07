from hkm.erpnext___custom.extend.hr.essl import eTimeTrackLite
from datetime import datetime
import frappe
from frappe.utils import today


def get_chekins():
    machine = eTimeTrackLite(domain="59.144.166.140:82")
    from_t = "2024-05-01"
    till = "2024-05-01"
    # from_t = today()
    # till = today()
    machine.set_request_body(
        {
            "from_time": from_t,
            "to_time": till,
            "serial_no": "AF39202660402",
            # "username": "erp",
            # "password": "************",
        }
    )
    machine.fetch_logs()
    # print(machine.logs)
    # print([x for x in machine.logs if x[0] == "198"])
    employee_map = {}
    for employee in frappe.get_all(
        "Employee",
        fields=["name", "attendance_device_id"],
        filters={"status": "Active"},
    ):
        employee_map.setdefault(employee["attendance_device_id"], employee["name"])
    length = len(machine.logs)
    for ind, log in enumerate(machine.logs):
        # print(f"Operation : {ind}/{length}")
        if log[0] in employee_map:
            checkin_doc = frappe.get_doc(
                {
                    "doctype": "Employee Checkin",
                    "employee": employee_map[log[0]],
                    "time": log[1],
                }
            )
            checkin_doc.insert()
    frappe.db.commit()


def clean_attendance():

    for ind, a in enumerate(frappe.get_all("Attendance", pluck="name")):
        print(f"Operation : {ind}")
        doc = frappe.get_doc("Attendance", a)
        if doc.docstatus == 1:
            doc.cancel()
            doc.delete(delete_permanently=True)
        elif doc.docstatus == 2:
            doc.delete(delete_permanently=True)

    frappe.db.commit()


def clean_checkins():

    for ind, a in enumerate(
        frappe.get_all(
            "Employee Checkin",
            # filters={"creation": (">=", "2024-04-21 00:00:00")},
            pluck="name",
        )
    ):
        doc = frappe.get_doc("Employee Checkin", a)
        doc.delete(delete_permanently=True)

    frappe.db.commit()
