// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.query_reports["Sales Suspense"] = {
	"filters": [
		{
			"fieldname": "company",
			"label": __("Company"),
			"fieldtype": "Link",
			"width": "80",
			"options": "Company",
			"reqd": 1,
			"default": frappe.defaults.get_user_default("Company"),
		},
		/*{
			"fieldname":"jv_entry",
			"label": __("Suspense Entry"),
			"fieldtype": "Link",
			"options":'Journal Entry',
			"width": "80",
			"get_query": function() {
				return {
					"query": "custom_app.extend.queries.suspense_voucher_query"
				}
			},
		},*/
		{
			"fieldname": "from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			//"reqd": 1,
			"default": "2022-04-01",
			"read_only": 1
		},
		{
			"fieldname": "to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			"default": frappe.datetime.get_today(),
		},
		{
			"fieldname": "status",
			"label": __("Status"),
			"fieldtype": "Select",
			"options": ['All', 'Cleared', 'Partially Cleared', 'Uncleared', 'Mismatched', 'Unlinked'],
			"width": "80",
			"default": "Uncleared",
			"on_change": function () {
				let status = frappe.query_report.get_filter_value('status');
				let show_new = frappe.query_report.get_filter_value('show_new');
				let show = (status === "Uncleared") && show_new
				frappe.query_report.toggle_filter_display('sort', !show);
				frappe.query_report.refresh();
			}
		},/*
		{
			"label": __("Group By JV"),
			"fieldname": "group_jv",
			"fieldtype": "Check",
			"width": "80",
			"default": 0,
		},*/
		{
			"label": __("New"),
			"fieldname": "show_new",
			"fieldtype": "Check",
			"default": 0,
			"on_change": function () {
				let status = frappe.query_report.get_filter_value('status');
				let show_new = frappe.query_report.get_filter_value('show_new');
				let show = (status === "Uncleared") && show_new
				frappe.query_report.toggle_filter_display('sort', !show);
				frappe.query_report.refresh();
			},
		},
		{
			"label": __("Sort By Amount"),
			"fieldname": "sort",
			"fieldtype": "Check",
			"default": 0,
		},
	],
	"formatter": function (value, row, column, data, default_formatter) {
		value = default_formatter(value, row, column, data);
		if (column && data && column.fieldname == "uncleared_amount") {
			const uncleared_amount = flt(data.uncleared_amount);
			const clearing_amt = flt(data.clearing_amt);
			const jv_amount = flt(data.jv_amount);
			if (uncleared_amount < 0) {
				value = "<span style='color:red'><b>" + value + "</b></span>";
			} else if (uncleared_amount === 0) {
				value = "<span style='color:green'>" + value + "</span>";
			} else if (clearing_amt > 0 && clearing_amt < jv_amount) {
				value = "<span style='color:orange'>" + value + "</span>";
			} else {
				value = "<span style='color:blue'>" + value + "</span>";
			}

		}
		return value;
	},
};