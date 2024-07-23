frappe.ui.form.on("Sales Invoice", {
  onload: function (frm) {
    frm.set_query("default_sales_income_account", function () {
      return {
        filters: { root_type: "Income", is_group: 0, company: frm.doc.company },
      };
    });

    frm.set_query("default_difference_cost_center", function () {
      return {
        filters: { is_group: 0, company: frm.doc.company },
      };
    });

    if (frm.doc.docstatus == 0) {
      frm.add_custom_button(
        __("Direct Trash"),
        function () {
          frappe.call({
            method: "hkm.erpnext___custom.common.directly_mark_cancelled",
            args: {
              doctype: frm.doc.doctype,
              docname: frm.doc.name,
            },
            callback: (r) => {
              frm.reload_doc();
            },
          });
        },
        "Actions"
      );
    }
  },
  before_save: function (frm) {
    if (frm.doc.default_sales_income_account) {
      frm.events.update_default_sales_income_account(frm);
    }
  },
  default_sales_income_account: function (frm) {
    frm.events.update_default_sales_income_account(frm);
  },
  default_difference_cost_center: function (frm) {
    frm.events.update_default_cost_center(frm);
  },
  update_default_sales_income_account(frm) {
    var entries = frm.doc.items;
    for (var i = 0; i < entries.length; i++) {
      frappe.model.set_value(
        "Sales Invoice Item",
        entries[i].name,
        "income_account",
        frm.doc.default_sales_income_account
      );
    }
    frm.refresh_field("items");
  },
  update_default_cost_center(frm) {
    var entries = frm.doc.items;
    for (var i = 0; i < entries.length; i++) {
      frappe.model.set_value(
        "Sales Invoice Item",
        entries[i].name,
        "cost_center",
        frm.doc.default_difference_cost_center
      );
    }
    frm.set_value("cost_center", frm.doc.default_difference_cost_center);
    frm.refresh_field("items");
  },
});
