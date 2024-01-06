frappe.ui.form.on("Material Request", {
    onload(frm){
        frm.set_query('custom_site_supervisor', function(frm){
            return{
                filters:{
                    custom_is_supervisor:1
                }
            }
        })
        frm.set_query('custom_cost_center', function(frm){
            return{
                filters:{
                    is_group:0,
                    disabled:0
                }
            }
        })
    }
})