# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class MaterialConsumptionEntry(Document):
	def on_submit(self):
		se_doc = frappe.new_doc("Stock Entry")
		se_doc.stock_entry_type = "Material Issue"
		se_doc.from_warehouse = self.project_warehouse
		mcd = frappe.db.get_all("Material Consumption Details",{"parent": self.name},
		["item_name as item_code", "qty", "uom", "uom as stock_uom"])
		for item in mcd:
			item["cost_center"] = self.cost_center
			item["s_warehouse"] = self.project_warehouse
			item["conversion_factor"] = 1
			se_doc.append("items", item)
		se_doc.save(ignore_permissions=True)
		se_doc.submit()

