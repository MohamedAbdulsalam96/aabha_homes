// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Workers Wages Balance", {
	refresh(frm) {
        if(frm.doc.docstatus == 1)
        frm.add_custom_button(
            __("Journal Entry"), function(){
                if(!frm.doc.balance_amount){
                    frappe.throw("Nothing is pending!")
                }
                frappe.confirm(__("Proceed to create Journal Entry?"), function() {
					frappe.xcall("aabha_homes.aabha_homes.utils.create_wb_je", {
                        name: frm.doc.name,
                        emp: frm.doc.worker_name,
                        amt: frm.doc.balance_amount,
                        costCenter: frm.doc.cost_center,
                        refDate: frm.doc.date
                    }).then(data=>{
                        if(data){
                            frm.refresh_field("balance_amount")
                            frappe.msgprint("Journal Enrty Created Successfully")
                        }
                    })
				});
            },
            __("Create"))
	},
});
