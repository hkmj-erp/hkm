// Copyright (c) 2024, Narahari Dasa and contributors
// For license information, please see license.txt

frappe.ui.form.on("HKM HR Operations", {
	refresh(frm) {

	},
    fetch_c_offs:function(frm){
        if(frm.is_dirty()){
            frappe.throw("Please save before clicking on this.");
        }else{
            frappe.call({
                freeze:true,
                freeze_message:"Creating Comp-Offs",
                method: "hkm.erpnext___custom.doctype.hkm_hr_operations.leaves.create_comp_off_for_weekoff_present",
                callback: function(r) {
                    if(!r.exc){
                        frappe.msgprint("Created Successfully. Please Check Once.");
                    }
                }
            });
        }
		
	}
});


