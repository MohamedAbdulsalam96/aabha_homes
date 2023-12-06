import frappe
from datetime import date

@frappe.whitelist()
@frappe.validate_and_sanitize_search_inputs
def get_se_cc(doctype, txt, searchfield, start, page_len, filters):
    swa_cc = frappe.db.sql("""
        SELECT cost_center
        FROM `tabSite Worker Assignment` SWA
        WHERE
            supervisor_name = '{0}' and
            status = "Active" and
            docstatus = 1
    """.format(filters.get("supervisor_name"), filters.get("posting_date")))
    swa_cc = set(swa_cc)
    return swa_cc