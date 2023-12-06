import frappe
from datetime import date
from frappe.model.mapper import get_mapped_doc

@frappe.whitelist()
def site_entry_emp(costCenter, postingDate):
	"""
	swa = site worker entry
	"""
	if not frappe.db.exists("Site Worker Assignment", {"status":"Active", "cost_center":costCenter, "docstatus": 1}):
		frappe.throw("Couldn't find Site Worker Assignment")
	swa = frappe.get_last_doc("Site Worker Assignment", 
	{"status":"Active", "cost_center":costCenter, "docstatus": 1})
	swa_emp = frappe.db.get_list("Worker Assignment Details", {"parent": swa.name},
	["workers"], pluck="workers", ignore_permissions=True)
	if not swa_emp:
		frappe.throw("Couldn't find assigned workers")
	wage_data = []
	for emp in swa_emp:
		ws_doc = frappe.db.sql("""
			SELECT
				name,
				basic_amount,
				worker_name,
				basic_amount as net_pay,
				normal_working_hours,
				overtime_factor
			FROM 
				`tabWage Structure` WS
			WHERE
				worker_name = '{0}' and
				docstatus = 1 and
				as_on_date <= '{1}'
			ORDER BY
				as_on_date DESC
			LIMIT 1
		""".format(emp, postingDate),
		as_dict=True)
		if ws_doc:
			wage_data.append(ws_doc[0])
		else:
			frappe.throw("Couldn't find Wage structure for {0}".format(emp))
	return wage_data
			
@frappe.whitelist()
def get_total_emp_wages(costCenter):
	if not frappe.db.exists("Site Entry", {"cost_center": costCenter, "docstatus":1}):
		frappe.throw("No 'Site Entry' found")
	query = make_se_query(costCenter) or ""
	if not query:
		frappe.msgprint("No unpaid worker found from {0}".format(costCenter))
		return
	data = frappe.db.sql("""
		SELECT 
			SUM(basic_amount) as total_wages_amount,
			SUM(overtime_amount) as total_overtime_amount,
			sum(net_pay) as net_pay,
			sum(net_pay) as original_net_pay,
			SUM(overtime) as total_overtime_hours,
			worker_name as workers_name
		FROM `tabWorkers Details` WD
		{query}
		GROUP BY worker_name
	""".format(query=query), as_dict=True)
	for d in data:
		if frappe.db.exists("Workers Wages Balance",{"worker_name":d.workers_name, "cost_center": costCenter}):
			d["previous_balance"] = frappe.db.get_value("Workers Wages Balance",
			{"worker_name":d.workers_name, "cost_center": costCenter}, ["balance_amount"])
			if d.get("previous_balance"):
				d["original_net_pay"] = d.get("net_pay") + d.get("previous_balance")
				d["net_pay"] = d.get("net_pay") + d.get("previous_balance")

	data_split = frappe.db.sql("""
		SELECT 
			WD.worker_name as workers_name,
			WD.basic_amount,
			WD.overtime_amount,
			WD.net_pay,
			WD.overtime,
			SE.name as site_entry_reference,
			SE.posting_date as site_entry_date,
			WD.name as workers_details_doc,
			WD.docstatus
		FROM `tabWorkers Details` WD
		INNER JOIN 	`tabSite Entry` SE
		ON WD.parent = SE.name
		{query}
		ORDER BY WD.worker_name
	""".format(query=query), as_dict=True)
	return {"data": data, "data_split": data_split}

def make_se_query(costCenter):
	paid_wd = []
	unpaid_wd = []
	query = ""
	sw_list = frappe.db.get_list("Site Wages", {"cost_center": costCenter, "docstatus":1},
	pluck="name", ignore_permissions=True)
	if sw_list:
		paid_wd = frappe.db.get_list("Site Wages Project Wise Total",
		{"docstatus":1, "parent": ["in", sw_list]}, ["workers_details_doc"], pluck="workers_details_doc",
		ignore_permissions=True)
	if paid_wd:
		se_list = frappe.db.get_list("Site Entry", {"cost_center": costCenter, "docstatus":1},
		pluck="name", ignore_permissions=True)
		unpaid_wd = frappe.db.get_list("Workers Details", 
		{"docstatus":1, "parent": ["in", se_list], "name": ["not in", paid_wd]},
		pluck="name", ignore_permissions=True)
	else:
		se_list = frappe.db.get_list("Site Entry", {"cost_center": costCenter, "docstatus":1},
		pluck="name", ignore_permissions=True)
		unpaid_wd = frappe.db.get_list("Workers Details", 
		{"docstatus":1, "parent": ["in", se_list]},
		pluck="name", ignore_permissions=True)
	if unpaid_wd:
		if len(unpaid_wd) == 1:
			query = """
				WHERE WD.name IN ('{unpaid_wd}')
			""".format(unpaid_wd=unpaid_wd[0])
		if len(unpaid_wd) > 1:
			query = """
				WHERE  WD.name IN {unpaid_wd}
			""".format(unpaid_wd=tuple(unpaid_wd))
	return query


@frappe.whitelist()
def create_wb_je(name, emp, amt, costCenter, refDate):
	credit_acc = frappe.db.get_single_value("Aabha Homes Settings", "wages_payable_account")
	debit_acc = frappe.db.get_single_value("Aabha Homes Settings", "wages_expense_account")
	if not credit_acc or not debit_acc:
		frappe.throw("Please Setup Aabha Homes Settings")
	je_doc = frappe.new_doc("Journal Entry")
	accounts = [{
		"account": credit_acc,
		"party_type": "Employee",
		"party": emp,
		"cost_center": costCenter,
		"credit_in_account_currency": amt
	},
	{
		"account": debit_acc,
		"party_type": "Employee",
		"party": emp,
		"cost_center": costCenter,
		"debit_in_account_currency": amt
	}]
	for acc in accounts:
		je_doc.append("accounts", acc)
	je_doc.posting_date = date.today()
	je_doc.cheque_no = name
	je_doc.cheque_date = refDate
	je_doc.save(ignore_permissions=True)
	je_doc.submit()

	if je_doc.name:
		frappe.db.set_value("Workers Wages Balance", name, "balance_amount", 0)
		return True
	else:
		return False

@frappe.whitelist()
def make_material_consumption(source_name, target_doc=None):
	doc = get_mapped_doc(
		"Purchase Receipt",
		source_name,
		{
			"Purchase Receipt": {"doctype": "Stock Entry", "validation": {"docstatus": ["=", 1]}},
			"Purchase Receipt Item": {
				"doctype": "Material Consumption Details",
				"field_map": {"qty": "qty","uom":"uom"},
			},
		},
		target_doc,
	)

	return doc
