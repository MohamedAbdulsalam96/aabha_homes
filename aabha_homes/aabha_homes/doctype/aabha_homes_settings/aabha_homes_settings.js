// Copyright (c) 2023, sammish and contributors
// For license information, please see license.txt

frappe.ui.form.on("Aabha Homes Settings", {
	onload(frm) {
        frm.set_query('wages_advance', function(frm){
            return{
                filters:{
                    root_type:"Asset",
                    account_type: "Payable"
                }
            }
        })
	},
});
