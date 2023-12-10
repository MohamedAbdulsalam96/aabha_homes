# Copyright (c) 2023, sammish and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from datetime import date


class SiteWages(Document):
	def before_submit(self):
		self.create_je()
		self.set_pending()
		self.create_wage_slip()

	def on_cancel(self):
		if frappe.db.exists("Wages Slip",
		{"site_wages":self.name, "docstatus": ["=", "1"]}):
			ws_list = frappe.db.get_list("Wages Slip",
			{"site_wages":self.name, "docstatus": ["=", "1"]}, pluck="name")
			for ws in ws_list:
				ws_doc = frappe.get_doc("Wages Slip", ws)
				ws_doc.cancel()

		je = frappe.db.exists("Journal Entry",
		{"cheque_no":self.name, "docstatus": ["=", "1"]})
		if je:
			je_doc = frappe.get_doc("Journal Entry", je)
			je_doc.cancel()

		for row in self.site_wages_details:
			wwb = frappe.db.exists("Workers Wages Balance",
			{"cost_center": self.cost_center, "worker_name": row.workers_name, "docstatus": ["!=", "2"]})
			if wwb and row.previous_balance:
				wwb_doc = frappe.get_doc("Workers Wages Balance", wwb)
				wwb_doc.balance_amount = row.previous_balance
				wwb_doc.save(ignore_permissions=True)
				
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
				emp["cost_center"] = self.cost_center
				je_doc.append("accounts", emp)
			je_doc.append("accounts", {
				"account": debit_acc, 
				"debit_in_account_currency": debit_amount, 
				"cost_center": self.cost_center
			})
		je_doc.save(ignore_permissions=True)
		je_doc.submit()

	def set_pending(self):
		for row in self.site_wages_details:
			wwb_doc = None
			if frappe.db.exists("Workers Wages Balance",
			{"cost_center": self.cost_center, "worker_name": row.workers_name, "docstatus": ["!=", "2"]}):
				wwb_doc = frappe.get_last_doc("Workers Wages Balance",
				{"cost_center": self.cost_center, "worker_name": row.workers_name})
			else:
				wwb_doc = frappe.new_doc("Workers Wages Balance")
			wwb_doc.date = date.today()
			wwb_doc.cost_center = self.cost_center
			wwb_doc.worker_name = row.workers_name
			wwb_doc.balance_amount = row.balance
			wwb_doc.save(ignore_permissions=True)
			wwb_doc.submit()

	def create_wage_slip(self):
		for row in self.site_wages_details:
			slip_doc = frappe.new_doc("Wages Slip")
			slip_doc.cost_center = self.cost_center
			slip_doc.supervisor_name = frappe.db.get_value("Site Entry", 
			{"cost_center":self.cost_center, "docstatus":1}, "supervisor_name")
			slip_doc.posting_date = date.today()
			slip_doc.workers_name = row.workers_name
			split_details = frappe.db.get_all("Site Wages Project Wise Total",
			{"parent": self.name, "workers_name": row.workers_name},
			["site_entry_reference as ref", "net_pay", "overtime_amount", "overtime", "basic_amount", "site_entry_date as ref_date"])
			for detail in split_details:
				slip_doc.append("wages_slip_details", detail)
			bt = frappe.db.get_value("Site Wages Project Wise Total",
			{"parent": self.name, "workers_name": row.workers_name},
			["SUM(basic_amount)", "SUM(overtime_amount)", "SUM(overtime)"])
			swd = frappe.db.get_value("Site Wages Details",
			{"parent": self.name, "workers_name": row.workers_name},
			["previous_balance", "net_pay", "balance"])
			slip_doc.previous_balance = swd[0]
			slip_doc.site_wages = self.name
			slip_doc.balance = swd[2]
			slip_doc.total_paid = swd[1]
			slip_doc.grand_total = bt[0] + bt[1] + swd[0]
			slip_doc.total_overtime_amount = bt[1]
			slip_doc.total_overtime = bt[2]
			slip_doc.save(ignore_permissions=True)
			slip_doc.submit()



