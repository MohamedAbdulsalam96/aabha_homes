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
        if(frm.doc.cost_center && !frm.doc.skip_site_worker_assignment){
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
        if(frm.doc.skip_site_worker_assignment){
            frm.set_value("site_worker_assignment", "")
        }
    },
    posting_date(frm){
        frm.set_value("cost_center", "")
        frm.set_value("workers_details", "")
    }
});


frappe.ui.form.on("Workers Details", {
    overtime(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let basic_amount = row.basic_amount
        let ta = row.ta || 0.0
        if(row.half_day){
            basic_amount = row.basic_amount/2
        }
        row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
        row.net_pay = row.overtime_amount + basic_amount + ta
        frm.refresh_field("workers_details")
    },
    half_day(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let ta = row.ta || 0.0
        let overtime_amount = row.overtime_amount || 0.0
        if(row.half_day){
            let basic_amount = row.basic_amount/2
            row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
            row.net_pay = overtime_amount + basic_amount + ta
            frm.refresh_field("workers_details")
        }else{
            row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
            row.net_pay = overtime_amount + row.basic_amount + ta
            frm.refresh_field("workers_details")
        }
        frm.refresh_fields("workers_details")
    },
    worker_name(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        if(row.worker_name){
            frappe.xcall("aabha_homes.aabha_homes.utils.get_wage_structure_details", {
                employee: row.worker_name,
                postingDate: frm.doc.posting_date
            }).then(data=>{
                if(data){
                    data = data[0]
                    row.basic_amount = data.basic_amount
                    row.overtime_factor = data.overtime_factor
                    row.normal_working_hours = data.normal_working_hours
                    row.net_pay = data.basic_amount
                    row.overtime_amount = 0.0
                    row.overtime = 0.0
                    frm.refresh_field("workers_details")
                }
            })
        }
    },
    ta(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let ta = row.ta || 0.0
        let overtime = row.overtime || 0.0
        if(row.below_half_day){
            row.net_pay = row.below_half_day_amount + row.ta
        }
        else if(!row.below_half_day){
            if(row.half_day){
                let basic_amount = row.basic_amount/2
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * overtime
                row.net_pay = row.overtime_amount + basic_amount + ta
            }else{
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * overtime
                row.net_pay = row.overtime_amount + row.basic_amount + ta
            }
        }
        frm.refresh_fields("workers_details")
    },
    below_half_day(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        if(row.below_half_day){
            row.half_day = false
            row.net_pay = 0
            row.overtime = 0
            row.overtime_amount = 0
        }else{
            let ta = row.ta || 0.0
            row.below_half_day_amount = 0
            if(row.half_day){
                let basic_amount = row.basic_amount/2
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
                row.net_pay = row.overtime_amount + basic_amount + ta
            }else{
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
                row.net_pay = row.overtime_amount + row.basic_amount + ta
            }
        }
        frm.refresh_fields("workers_details")
    },
    below_half_day_amount(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let ta = row.ta || 0.0
        if(row.below_half_day){
            row.net_pay = row.below_half_day_amount + ta
        }
        else if(!row.below_half_day){
            if(row.half_day){
                let basic_amount = row.basic_amount/2
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
                row.net_pay = row.overtime_amount + basic_amount + ta
            }else{
                row.overtime_amount = (row.basic_amount/row.normal_working_hours) * row.overtime_factor * row.overtime
                row.net_pay = row.overtime_amount + row.basic_amount + ta
            }
        }
        frm.refresh_fields("workers_details")
    }
})