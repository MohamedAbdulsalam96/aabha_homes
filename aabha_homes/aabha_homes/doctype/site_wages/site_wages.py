# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date


class SiteWages(Document):
	def before_submit(self):
		self.create_je()
	def create_je(self):
		je_doc = frappe.new_doc("Journal Entry")
		je_doc.company = frappe.defaults.get_defaults().company
		je_doc.posting_date = date.today()
		emp_list = frappe.db.get_all("Site Wages Details", {"parent": self.name},
		["workers_name as party", "net_pay as credit_in_account_currency"])
		credit_acc = frappe.db.get_single_value("Aabha Homes Settings", "wages_payable_account")
		debit_acc = frappe.db.get_single_value("Aabha Homes Settings", "wages_expense_account")
		debit_amount = frappe.db.get_value("Site Wages Details", 
		{"parent":self.name}, ["SUM(net_pay)"])
		if not credit_acc or not debit_acc:
			frappe.throw("Please Setup Aabha Homes Settings")
		if emp_list:
			for emp in emp_list:
				emp["party_type"] = "Employee"
				emp["account"] = credit_acc
				je_doc.append("accounts", emp)
			je_doc.append("accounts", 
			{"account": debit_acc, "debit_in_account_currency": debit_amount})
		je_doc.save(ignore_permissions=True)

