from frappe import _

def get_data():
    return {
		"fieldname": "site_entry",
        "non_standard_fieldnames": {
			"Site Wages": "site_entry_reference",
		},
        "internal_links": {
			"Site Worker Assignment": "site_worker_assignment"
		},
		"transactions": [
			{"label": _("Site Worker Assignment"), "items": ["Site Worker Assignment"]},
            {"label": _("Site Wages"), "items": ["Site Wages"]},
		],
	}