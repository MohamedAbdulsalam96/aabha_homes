// Copyright (c) 2024, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Running Cost Entry", {
	get_gl_entry(frm) {
        frappe.call({
            method:"get_gl_entry",
            doc:frm.doc,
            callback:function(r){
                frm.set_value("running_cost_gl_item", "")
                frm.set_value("total_project_amount", 0)
                frm.set_value("running_cost_project_item", "")
                let gl_list = r.message.gl_list
                let total_project_amount = r.message.total_debit_amount[0].total_debit_amount
                let running_cost_project_item = r.message.cost_center_wise_debit
                gl_list.forEach(element => {
                    frm.add_child("running_cost_gl_item", element)
                });
                frm.refresh_field("running_cost_gl_item")
                frm.doc.total_project_amount = total_project_amount
                frm.refresh_field("total_project_amount")
                running_cost_project_item.forEach(element => {
                    frm.add_child("running_cost_project_item", element)
                });
                frm.refresh_field("running_cost_project_item")
            }
        })
	},
    get_running_cost(frm){
        frappe.call({
            method:"get_running_cost",
            doc:frm.doc,
            callback:function(r){
                let rc_gl_list = r.message.rc_gl_list
                let trc = r.message.total_running_cost[0].total_running_cost
                rc_gl_list.forEach(element => {
                    frm.add_child("running_cost_item", element)
                });
                frm.refresh_field("running_cost_item")
                frm.doc.total_running_cost = trc
                frm.refresh_field("total_running_cost")
                if(trc > 0){
                    frappe.dom.freeze(__("Calculating running project amount..."))
                    frm.doc.running_cost_project_item.forEach(item=>{
                        item.running_project_amount = (trc * item.project_percentage)/100
                    })
                    frm.refresh_field("running_cost_project_item")
                    frappe.dom.unfreeze();
                }
            }
        })
    },
    onload(frm){
        if(frm.doc.docstatus == 0){
            frappe.db.get_doc("Aabha Homes Settings").then(data=>{
                frm.doc.running_cost_head = data.default_running_cost_assets
                frm.doc.running_cost_expense = data.default_running_cost_expense   
                frm.refresh_field("running_cost_head")
                frm.refresh_field("running_cost_expense")
            })
        }
    }
});

frappe.ui.form.on("Running Cost GL Item", {
    running_cost_gl_item_remove(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        let gl_list = []
        frm.doc.running_cost_gl_item.forEach(item=>{
            gl_list.push(item.gl_entry)
        })
        frappe.call({
            method:"get_gl_entry",
            doc:frm.doc,
            args:{
                gl_list: gl_list
            },
            callback:function(r){
                frm.set_value("running_cost_gl_item", "")
                frm.set_value("total_project_amount", 0)
                frm.set_value("running_cost_project_item", "")
                let gl_list = r.message.gl_list
                let total_project_amount = r.message.total_debit_amount[0].total_debit_amount
                let running_cost_project_item = r.message.cost_center_wise_debit
                gl_list.forEach(element => {
                    frm.add_child("running_cost_gl_item", element)
                });
                frm.refresh_field("running_cost_gl_item")
                frm.doc.total_project_amount = total_project_amount
                frm.refresh_field("total_project_amount")
                running_cost_project_item.forEach(element => {
                    frm.add_child("running_cost_project_item", element)
                });
                frm.refresh_field("running_cost_project_item")
            }
        })
    }
})