# Copyright (c) 2024, sammish and contributors
# For license information, please see license.txt

import frappe
from datetime import datetime, date
from frappe.model.document import Document


class RunningCostEntry(Document):
	@frappe.whitelist()
	def get_gl_entry(self, gl_list=None):
		filters = ""
		rcgl_list = frappe.db.get_list(
			"Running Cost GL Item",
			{
				"docstatus": 1,
				"parenttype": "Running Cost Entry"
			},
			[
				"gl_entry"
			],
			pluck="gl_entry",
			ignore_permissions=True
		)
		if len(rcgl_list) == 1:
			filters += "AND GLE.name != '{0}'".format(rcgl_list[0])
		elif len(rcgl_list) > 1:
			filters += "AND GLE.name NOT IN {0}".format(tuple(rcgl_list))
		if not self.date:
			frappe.throw("Date is mandatory!")
		if gl_list:
			if len(gl_list) == 1:
				filters += "AND GLE.name = '{0}'".format(gl_list[0])
			elif len(gl_list) > 1:
				filters += "AND GLE.name IN {0}".format(tuple(gl_list))
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
				{filters}
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month,
			filters=filters
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
				{filters}
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month,
			filters=filters
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
			month=datetime.strptime(self.date, "%Y-%m-%d").month,
			filters=filters
		), as_dict=True)
		cost_center_wise_debit = 0
		cost_center_wise_debit = frappe.db.sql("""
			SELECT 
				GLE.name as gl_entry,
				GLE.posting_date,
				SUM(GLE.debit) AS project_amount,
				GLE.cost_center AS project_cost_center,
				(SUM(GLE.debit)/{tpc})*100 AS project_percentage,
				0 AS running_project_amount
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
				{filters}
			GROUP BY
				GLE.cost_center
		""".format(
			month=datetime.strptime(self.date, "%Y-%m-%d").month,
			tpc = total_debit_amount[0].total_debit_amount or 0,
			trc = total_running_cost[0].total_running_cost or 0,
			filters = filters
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
		je_doc.custom_running_cost_entry = self.name
		je_doc.posting_date = self.date
		je_doc.cheque_date = self.date
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

	def on_cancel(self):
		je = frappe.db.exists("Journal Entry", {"cheque_no": self.name, "docstatus": 1})
		if je:
			frappe.throw("Linked with journal entry {0}. Cannot cancel!".format(je))