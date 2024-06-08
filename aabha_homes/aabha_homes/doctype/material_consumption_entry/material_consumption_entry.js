// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material Consumption Entry", {
    refresh(frm){
        setTimeout(() => {
            frm.refresh_field("items")
            if(frm.doc.material_consumption_details && frm.is_dirty() && frm.doc.project_warehouse){
                frappe.xcall("aabha_homes.aabha_homes.utils.get_bin_stock_list", {
                    doc: frm.doc.material_consumption_details,
                    warehouse: frm.doc.project_warehouse
                }).then(data=>{
                    if(data){
                        frm.set_value("material_consumption_details", data)
                    }
                })
            }
        }, 1000)
    },
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
                    is_group:0,
                    disabled:0
                }
            }
        })
	},
	get_from_purchase_receipt(frm) {
        if(!frm.doc.project_warehouse){
            frappe.throw("Please select project warehouse")
        }
        erpnext.utils.map_current_doc({
            method: "aabha_homes.aabha_homes.utils.make_material_consumption",
            source_doctype: "Purchase Receipt",
            target: frm,
            date_field: "posting_date",
            setters: {
                supplier: frm.doc.supplier || undefined,
                cost_center: frm.doc.cost_center || undefined,
            },
            get_query_filters: {
                docstatus: 1
            }
        })
	},
    cost_center(frm){
        if(frm.doc.cost_center){
            frappe.xcall("aabha_homes.aabha_homes.utils.site_entry_emp", {
                costCenter:frm.doc.cost_center,
                postingDate: frm.doc.posting_date
            }).then(data=>{
                if(data){
                    frm.set_value("supervisor_name", data.supervisor)
                }
            })
        }
    }
});

frappe.ui.form.on("Material Consumption Details", {
    item_name(frm, cdt, cdn){
        let row = locals[cdt][cdn]
        if(!frm.doc.project_warehouse){
            row.item_name = ""
            frm.refresh_fields("material_consumption_details")
            frappe.throw("Please select project warehouse")
        }
        if(row.item_name){
            frappe.xcall("aabha_homes.aabha_homes.utils.get_bin_stock", {
                item_code: row.item_name,
                warehouse: frm.doc.project_warehouse
            }).then(data=>{
                if(data.available_qty){
                    row.available_qty = data.available_qty
                }else{
                    row.available_qty = 0
                }
                row.uom = data.uom
                frm.refresh_fields("material_consumption_details")
            })
        }
    }
});
