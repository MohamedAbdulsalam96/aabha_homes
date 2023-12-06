# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SiteWorkerAssignment(Document):
	def on_submit(self):
		prev_doc = frappe.db.exists("Site Worker Assignment",
		{"cost_center": self.cost_center, "status": "Active", "name": ["!=", self.name]})
		print(prev_doc)
		if prev_doc:
			frappe.db.set_value("Site Worker Assignment", prev_doc, "status", "Inactive")
