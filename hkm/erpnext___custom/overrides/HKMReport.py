import datetime
import frappe
from frappe.core.doctype.report.report import Report, enable_prepared_report


class HKMReport(Report):
    def execute_script_report(self, filters):
        # save the timestamp to automatically set to prepared
        threshold = 150
        res = []

        start_time = datetime.datetime.now()

        # The JOB
        if self.is_standard == "Yes":
            res = self.execute_module(filters)
        else:
            res = self.execute_script(filters)

        # automatically set as prepared
        execution_time = (datetime.datetime.now() - start_time).total_seconds()
        if execution_time > threshold and not self.prepared_report:
            frappe.enqueue(enable_prepared_report, report=self.name)

        frappe.cache.hset("report_execution_time", self.name, execution_time)

        return res