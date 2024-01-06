// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Wages Advance", {
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
        frm.set_query('worker_name', function(frm){
            return{
                filters:{
                    custom_is_worker:1
                }
            }
        })
        frm.set_query('paid_to', function(frm){
            return{
                filters:{
                    root_type:"Asset",
                    account_type: "Payable"
                }
            }
        })
        if(!frm.doc.paid_to){
                frappe.db.get_single_value("Aabha Homes Settings", "wages_advance").then(data=>{
                frm.set_value("paid_to", data)
            })
        }
	},
    supervisor_name(frm){
        frm.set_value("paid_from", "")
        frappe.db.get_value("Employee", frm.doc.supervisor_name, ["petty_cash_account"]).then(data=>{
            frm.set_value("paid_from", data.message.petty_cash_account)
        })
    },
    before_save(frm){
        if(frm.is_new()){
            frm.doc.status = "Draft"
            frm.doc.site_wages = ""
        }
    }
});
