from frappe import _

def get_data():
	return {
		"fieldname": "site_worker_assignment",
		"non_standard_fieldnames": {
			"Site Entry": "site_worker_assignment",
		},
		"transactions": [
			{"label": _("Site Entry"), "items": ["Site Entry"]},
		],
	}
