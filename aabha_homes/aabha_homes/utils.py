import frappe

@frappe.whitelist()
def site_entry_emp(costCenter):
	"""
	swa = site worker entry
	"""
	swa = frappe.get_last_doc("Site Worker Assignment", 
	{"status":"Active", "cost_center":costCenter, "docstatus": 1})
	if not swa:
		frappe.throw("Couldn't find Site Worker Assignment")
	swa_emp = frappe.db.get_list("Worker Assignment Details", {"parent": swa.name},
	["workers"], pluck="workers", ignore_permissions=True)
	if not swa_emp:
		frappe.throw("Couldn't find assigned workers")
	wage_data = []
	for emp in swa_emp:
		if not frappe.db.exists("Wage Structure", {"worker_name":emp, "docstatus":1}):
			frappe.throw("Couldn't find wage structure for {emp}".format(emp=emp))
		wage_data.append(frappe.db.get_value("Wage Structure",
		{"worker_name":emp, "docstatus":1}, ["basic_amount", "worker_name", "basic_amount as net_pay"], as_dict=True))
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
	print(data_split)
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
	print("paid_wd-----------------------------------------------")
	print(paid_wd)
	if paid_wd:
		se_list = frappe.db.get_list("Site Entry", {"cost_center": costCenter, "docstatus":1},
		pluck="name", ignore_permissions=True)
		print("se_list-----------------------------------")
		print(se_list)
		unpaid_wd = frappe.db.get_list("Workers Details", 
		{"docstatus":1, "parent": ["in", se_list], "name": ["not in", paid_wd]},
		pluck="name", ignore_permissions=True)
	else:
		se_list = frappe.db.get_list("Site Entry", {"cost_center": costCenter, "docstatus":1},
		pluck="name", ignore_permissions=True)
		unpaid_wd = frappe.db.get_list("Workers Details", 
		{"docstatus":1, "parent": ["in", se_list]},
		pluck="name", ignore_permissions=True)
	print("unpaid-------------------------------------")
	print(unpaid_wd)
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
