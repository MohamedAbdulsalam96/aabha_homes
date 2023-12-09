from frappe import _

def get_data():
    return {
		"fieldname": "site_wages",
        "non_standard_fieldnames": {
			"Wages Slip": "site_wages",
            "Journal Entry": "cheque_no"
		},
        "internal_links": {
			"Site Entry": ["site_wages_project_wise_total", "site_entry_reference"],
		},
		"transactions": [
			{"label": _("Site Entry"), "items": ["Site Entry"]},
            {"label": _("Wages Slip"), "items": ["Wages Slip"]},
            {"label": _("Journal Entry"), "items": ["Journal Entry"]},
		],
	}