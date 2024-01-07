from frappe import _

def get_data():
    return {
		"fieldname": "wages_advance",
        "non_standard_fieldnames": {
            "Journal Entry": "cheque_no"
		},
        "internal_links": {
			"Site Wages": "site_wages",
			"Cost Center": "cost_center"
		},
		"transactions": [
            {"label": _("Site Wages"), "items": ["Site Wages"]},
            {"label": _("Journal Entry"), "items": ["Journal Entry"]},
		],
	}