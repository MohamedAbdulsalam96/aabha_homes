# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date


class SiteWages(Document):
	def before_submit(self):
		self.create_je()
		self.set_pending()
	def create_je(self):
		je_doc = frappe.new_doc("Journal Entry")
		je_doc.company = frappe.defaults.get_defaults().company
		je_doc.posting_date = date.today()
		je_doc.cheque_no = self.name
		je_doc.cheque_date = self.posting_date
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
		je_doc.submit()

	def set_pending(self):
		for row in self.site_wages_details:
			if row.balance:
				wwb_doc = frappe.new_doc("Workers Wages Balance")
				wwb.date = date.today()
				wwb.cost_center = self.cost_center
				wwb.worker_name = row.workers_name
				wwb.balace_amount = row.balance



