frappe.ui.form.on("Stock Entry", {
  onload: function (frm) {
    frm.set_query("default_difference_account", function () {
      return {
        filters: {
          root_type: "Expense",
          company: frm.doc.company,
          is_group: 0,
          disabled: 0,
        },
      };
    });
    frm.set_query("default_difference_cost_center", function () {
      return {
        filters: {
          disabled: 0,
          company: frm.doc.company,
          is_group: 0,
        },
      };
    });
  },
  default_difference_account: function (frm) {
    var entries = frm.doc.items;
    for (var i = 0; i < entries.length; i++) {
      frappe.model.set_value(
        "Stock Entry Detail",
        entries[i].name,
        "expense_account",
        frm.doc.default_difference_account
      );
    }
  },
  default_difference_cost_center: function (frm) {
    var entries = frm.doc.items;
    for (var i = 0; i < entries.length; i++) {
      frappe.model.set_value(
        "Stock Entry Detail",
        entries[i].name,
        "cost_center",
        frm.doc.default_difference_cost_center
      );
    }
  },
});

frappe.ui.form.on("Stock Entry Detail", {
  item_code: function (frm, cdt, cdn) {
    frappe.model.set_value(
      cdt,
      cdn,
      "expense_account",
      frm.doc.default_difference_account
    );
  },
});
