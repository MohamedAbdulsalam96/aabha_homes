// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Site Entry", {
	onload(frm) {
        frm.set_query('supervisor_name', function(frm){
            return{
                filters:{
                    custom_is_supervisor:1
                }
            }
        })
        frm.set_query('cost_center', function(frm){
            return{
                filters:{
                    is_group:0
                }
            }
        })
	},
    cost_center(frm){
        if(frm.doc.cost_center){
            frappe.xcall("aabha_homes.aabha_homes.utils.site_entry_emp", {
                costCenter:frm.doc.cost_center
            }).then(data=>{
                frm.set_value("workers_details", "")
                if(data){
                    data.forEach(d=>{
                        frm.add_child("workers_details", d)
                    })
                }
                frm.refresh_field("workers_details")
            })
        }
    },
    before_save(frm){
        let gross_pay = 0
        frm.doc.workers_details.forEach(row=>{
            gross_pay += row.net_pay
        })
        frm.set_value("gross_pay", gross_pay)
    }
});


frappe.ui.form.on("Workers Details", {
    overtime(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        frappe.db.get_value("Wage Structure",
        {"worker_name":row.worker_name, "docstatus":1},
        ["overtime_factor"]).then(data=>{
            if(data){
                row.overtime_amount = row.basic_amount * data.message.overtime_factor * row.overtime
                row.net_pay = row.overtime_amount + row.basic_amount
                frm.refresh_field("workers_details")

            }
        })
    }
})