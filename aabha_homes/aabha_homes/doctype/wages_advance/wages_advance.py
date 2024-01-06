# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from datetime import date
from frappe.model.document import Document


class WagesAdvance(Document):
	def on_submit(self):
		self.status = "Submitted"
		credit_acc = self.paid_from
		debit_acc = self.paid_to
		if not credit_acc or not debit_acc:
			frappe.throw("Please Setup Aabha Homes Settings")
		je_doc = frappe.new_doc("Journal Entry")
		accounts = [
			{
				"account": debit_acc,
				"party_type": "Employee",
				"party": self.worker_name,
				"cost_center": self.cost_center,
				"debit_in_account_currency": self.advance_amount
			}	,
			{
				"account": credit_acc,
				"party_type": "Employee",
				"party": self.worker_name,
				"cost_center": self.cost_center,
				"credit_in_account_currency": self.advance_amount
			}
		]
		for acc in accounts:
			je_doc.append("accounts", acc)
		je_doc.posting_date = date.today()
		je_doc.cheque_no = self.name
		je_doc.cheque_date = date.today()
		je_doc.save(ignore_permissions=True)
		je_doc.submit()
	
	def on_cancel(self):
		if frappe.db.exists("Journal Entry", {"cheque_no": self.name}):
			je_doc = frappe.get_doc("Journal Entry", {"cheque_no": self.name})
			je_doc.cancel()
