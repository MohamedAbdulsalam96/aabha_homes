# Copyright (c) 2024, sammish and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, date
from frappe.model.document import Document


class RunningCostEntry(Document):
	@frappe.whitelist()
	def get_gl_entry(self):
		if not self.date:
			return
		gl_list = frappe.db.sql("""
			SELECT 
				GLE.name as gl_entry,
				GLE.posting_date,
				GLE.debit AS debit_amount,
				GLE.cost_center
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				GLE.debit > 0.00 AND
				ACC.custom_is_running_cost != 1
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month
		), as_dict=True)

		total_debit_amount = frappe.db.sql("""
			SELECT 
				SUM(GLE.debit) AS total_debit_amount
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				ACC.custom_is_running_cost != 1
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month
		), as_dict=True)

		total_running_cost = frappe.db.sql("""
			SELECT 
				SUM(GLE.debit) AS total_running_cost
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				ACC.custom_is_running_cost = 1
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month
		), as_dict=True)
		cost_center_wise_debit = 0
		cost_center_wise_debit = frappe.db.sql("""
			SELECT 
				GLE.name as gl_entry,
				GLE.posting_date,
				SUM(GLE.debit) AS project_amount,
				GLE.cost_center AS project_cost_center,
				(SUM(GLE.debit)/{tpc})*100 AS project_percentage,
				(SUM(GLE.debit)/{tpc})*100 + {trc} AS running_project_amount
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				GLE.debit > 0.00 AND
				ACC.custom_is_running_cost != 1
			GROUP BY
				GLE.cost_center
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month,
			tpc = total_debit_amount[0].total_debit_amount or 0,
			trc = total_running_cost[0].total_running_cost or 0
		), as_dict=True)
		return {"gl_list": gl_list, "total_debit_amount": total_debit_amount, "cost_center_wise_debit":cost_center_wise_debit}


	@frappe.whitelist()
	def get_running_cost(self):
		total_running_cost = frappe.db.sql("""
			SELECT 
				SUM(GLE.debit) AS total_running_cost
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				ACC.custom_is_running_cost = 1
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month
		), as_dict=True)

		rc_gl_list = frappe.db.sql("""
			SELECT 
				GLE.name as gl_entry,
				GLE.posting_date,
				GLE.debit AS debit_amount,
				GLE.cost_center
			FROM 
				`tabGL Entry` GLE
			INNER JOIN
				`tabAccount` ACC
			ON
				GLE.account = ACC.name
			WHERE 
				MONTH(GLE.posting_date) = {month} AND
				GLE.debit > 0.00 AND
				ACC.custom_is_running_cost = 1
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month
		), as_dict=True)

		return {"total_running_cost": total_running_cost, "rc_gl_list": rc_gl_list}

	def on_submit(self):
		if not self.running_cost_head or not self.running_cost_expense:
			frappe.throw("Running Cost Asset and Expense accounts are mandatory!")
		je_doc = frappe.new_doc("Journal Entry")
		je_doc.cheque_no = self.name
		je_doc.posting_date = date.today()
		je_doc.cheque_date = date.today()
		if not self.running_cost_project_item:
			frappe.throw("No running cost prject item found!")
		for item in self.running_cost_project_item:
			je_doc.append("accounts", {
					"account": self.running_cost_head,
					"cost_center": item.project_cost_center,
					"credit_in_account_currency": item.running_project_amount
				}
			)
			je_doc.append("accounts", {
				"account": self.running_cost_expense,
				"cost_center": item.project_cost_center,
				"debit_in_account_currency": item.running_project_amount
			})
		je_doc.insert()
		je_doc.submit()
		frappe.msgprint("Journal Entry {0} created.".format(je_doc.name))