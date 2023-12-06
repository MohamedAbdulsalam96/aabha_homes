// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Material Consumption Entry", {
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
        erpnext.utils.map_current_doc({
            method: "aabha_homes.aabha_homes.utils.make_material_consumption",
            source_doctype: "Purchase Receipt",
            target: frm,
            date_field: "posting_date",
            setters: {
                supplier: frm.doc.supplier || undefined,
                cost_center: frm.doc.cost_center || undefined,
                // set_warehouse: frm.doc.project_warehouse || undefined
            },
            get_query_filters: {
                docstatus: 1
            }
        })
	},
});
