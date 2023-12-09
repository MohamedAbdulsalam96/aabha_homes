# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SiteEntry(Document):
	def on_submit(self):
		self.status = "Completed"
	def on_cancel(self):
		sw_ref = frappe.db.exists("Site Wages Project Wise Total",
		{"site_entry_reference": self.name, "docstatus": ["=", "1"]})
		if sw_ref:
			sw = frappe.db.get_value("Site Wages Project Wise Total", sw_ref, ["parent"])
			sw_doc = frappe.get_doc("Site Wages", sw)
			if sw_doc.docstatus != 2:
				frappe.throw("{0} is linked with Site Wages {1}.\nPlease cancel it first.".format(self.name, sw))

