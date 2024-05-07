import frappe
from frappe.query_builder.functions import Count, Extract, Sum
from hrms.hr.utils import get_holidays_for_employee, get_holiday_list_for_employee
from frappe.utils import getdate
from datetime import datetime, timedelta
from calendar import monthrange, month_name
import copy
from .common import get_month_number

Filters = frappe._dict
COMPENSATORY_OFF = "Compensatory Off"


@frappe.whitelist()
def create_comp_off_for_weekoff_present():
    operations_doc = frappe.get_doc("HKM HR Operations")
    month = get_month_number(operations_doc.month)
    year = operations_doc.year
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    total_days = monthrange(year, month)[1]
    eligible_comp_offs = []
    for employee, days_map in get_employees_attendance_holidays_map(
        start_date, end_date, total_days
    ).items():
        for day, val in days_map.items():
            c_off_date = datetime(year, month, day)
            if val["holiday"] and val["present"]:
                eligible_comp_offs.append(
                    {
                        "employee": employee,
                        "work_from_date": c_off_date,
                        "work_end_date": c_off_date,
                        "leave_type": COMPENSATORY_OFF,
                        "reason": "Auto Generated from present on Week-Off.",
                    }
                )
    for e in eligible_comp_offs:
        c_off_doc = frappe.get_doc({"doctype": "Compensatory Leave Request", **e})
        c_off_doc.insert()
        c_off_doc.submit()

    frappe.db.commit()


def get_employees_attendance_holidays_map(start_date, end_date, total_days):

    holiday_list_map = get_holiday_list_map(start_date, end_date)

    day_map = {
        day: {"present": False, "holiday": False}
        for day in list(range(1, total_days + 1))
    }

    employees = {}

    for e in frappe.get_all("Employee", filters={"status": "Active"}, pluck="name"):
        employees.setdefault(e, copy.deepcopy(day_map))
        holiday_list = get_holiday_list_for_employee(e, raise_exception=True)
        for day in holiday_list_map[holiday_list]:
            employees[e][day]["holiday"] = True

    ##Set Attendance Records
    for r in get_attendance_records(
        filters=frappe._dict(
            month=4,
            year=2024,
            employees=list(employees.keys()),
            company="Hare Krishna Movement Jaipur",
        )
    ):
        if r["status"] == "Present":
            employees[r["employee"]][r["day_of_month"]]["present"] = True

    return employees


def get_attendance_records(filters: Filters) -> list[dict]:
    Attendance = frappe.qb.DocType("Attendance")
    query = (
        frappe.qb.from_(Attendance)
        .select(
            Attendance.employee,
            Extract("day", Attendance.attendance_date).as_("day_of_month"),
            Attendance.status,
        )
        .where(
            (Attendance.docstatus == 1)
            & (Attendance.company == filters.company)
            & (Extract("month", Attendance.attendance_date) == filters.month)
            & (Extract("year", Attendance.attendance_date) == filters.year)
            & (Attendance.employee.isin(filters.employees))
        )
    )
    query = query.orderby(Attendance.employee, Attendance.attendance_date)
    return query.run(as_dict=1)


def get_holiday_list_map(start_date, end_date):
    holiday_list_map = {}

    for h in frappe.db.sql(
        f"""
                    SELECT hdl.name as list_id, DAY(hd.holiday_date) as day
                    FROM `tabHoliday List` hdl
                    JOIN `tabHoliday`hd
                        ON hd.parent = hdl.name
                    WHERE hd.holiday_date BETWEEN '{start_date}' AND '{end_date}'
                    """,
        as_dict=1,
    ):
        if h["list_id"] not in holiday_list_map:
            holiday_list_map.setdefault(h["list_id"], [])
        holiday_list_map[h["list_id"]].append(h["day"])

    return holiday_list_map
