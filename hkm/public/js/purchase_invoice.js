frappe.ui.form.on("Purchase Invoice", {
  refresh: function (frm) {
    if (frm.doc.docstatus === 1) {
      frappe.call({
        method:
          "hkm.erpnext___custom.overrides.HKMPurchaseInvoice.get_documents_map_data",
        args: {
          document: frm.doc.name,
        },
        callback: function (r) {
          if (!r.exc) {
            frm.set_df_property("documents_map_html", "options", r.message);
          }
        },
      });
    }
  },
  onload: function (frm) {
    frm.set_query("default_difference_account", function () {
      return {
        filters: { root_type: "Expense", company: frm.doc.company },
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
  default_difference_account: function (frm) {
    var entries = frm.doc.items;
    for (var i = 0; i < entries.length; i++) {
      frappe.model.set_value(
        "Purchase Invoice Item",
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
        "Purchase Invoice Item",
        entries[i].name,
        "cost_center",
        frm.doc.default_difference_cost_center
      );
    }
    frm.set_value("cost_center", frm.doc.default_difference_cost_center);
  },
});

frappe.ui.form.on("Purchase Invoice Item", {
  item_code: function (frm, cdt, cdn) {
    frappe.model.set_value(
      cdt,
      cdn,
      "expense_account",
      frm.doc.default_difference_account
    );
  },
});
