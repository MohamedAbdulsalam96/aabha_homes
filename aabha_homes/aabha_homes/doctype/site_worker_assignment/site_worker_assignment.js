// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Site Worker Assignment", {
	onload(frm){
        frm.set_query('supervisor_name', function(frm){
            return{
                filters:{
                    custom_is_supervisor:1
                }
            }
        })
        frm.fields_dict['workers_details'].grid.get_field('workers').get_query = function(frm, cdt, cdn){
            return {
                filters:{
                    custom_is_worker:1
                }
            }
        }
        frm.set_query('cost_center', function(frm){
            return{
                filters:{
                    is_group:0
                }
            }
        })
	},
});
