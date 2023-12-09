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
        frm.fields_dict['workers_details'].grid.get_field('worker_name').get_query = function(frm, cdt, cdn){
            return {
                filters:{
                    custom_is_worker:1
                }
            }
        }
	},
    cost_center(frm){
        frm.set_value("workers_details", "")
        if(frm.doc.cost_center){
            frappe.xcall("aabha_homes.aabha_homes.utils.site_entry_emp", {
                costCenter:frm.doc.cost_center,
                postingDate: frm.doc.posting_date
            }).then(data=>{
                frm.set_value("workers_details", "")
                if(data){
                    data.wage_data.forEach(d=>{
                        frm.add_child("workers_details", d)
                    })
                    frm.set_value("supervisor_name", data.supervisor)
                    frm.set_value("site_worker_assignment", data.swa)
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
    },
    posting_date(frm){
        frm.set_value("cost_center", "")
        frm.set_value("workers_details", "")
    }
});


frappe.ui.form.on("Workers Details", {
    overtime(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
        row.net_pay = row.overtime_amount + row.basic_amount
        frm.refresh_field("workers_details")
    }
})