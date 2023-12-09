# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class SiteWorkerAssignment(Document):
	def on_cancel(self):
		se = frappe.db.exists("Site Entry",
		{"site_worker_assignment": self.name, "docstatus": ["!=" "2"]})
		if se:
			frappe.throw("{0} is linked with {1}".format(self.name, se))
