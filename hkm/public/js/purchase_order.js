frappe.ui.form.on("Purchase Order", {
  company: function (frm) {
    frm.set_query("department", () => {
      return {
        filters: {
          company: frm.doc.company,
        },
      };
    });
  },
});

frappe.ui.form.on("Purchase Order Item", {
  // The child table is defined in a DoctType called "Dynamic Link"
  item_code(frm, cdt, cdn) {
    // "links" is the name of the table field in ToDo, "_add" is the event

    let row = frappe.get_doc(cdt, cdn);
    if (row.item_code) {
      frappe.db.get_doc("Item", row.item_code).then((doc) => {
        if (doc.is_fixed_asset == 1) {
          row.item_type = "Asset";
        } else if (doc.is_stock_item == 1) {
          row.item_type = "Stock";
        } else {
          row.item_type = "Non-Stock";
        }
        frm.refresh_field("items");
      });
    }
  },
});
