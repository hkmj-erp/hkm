// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on('WhatsApp Message', {
	refresh: function (frm) {
		if (frm.doc.type == 'Incoming') {
			frm.add_custom_button(__("Reply"), function () {
				frappe.new_doc("WhatsApp Message", { "to": frm.doc.from });

			});
		}
	}
});
