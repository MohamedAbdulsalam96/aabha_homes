// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Wage Structure", {
	onload(frm) {
        frm.set_query('worker_name', function(frm){
            return{
                filters:{
                    custom_is_worker:1
                }
            }
        })
	},
});
