from frappe import _


def get_data():
	return {
		"fieldname": "custom_running_cost_entry",
        "external_links": {
			"Journal Entry": "custom_running_cost_entry"
		},
		"transactions": [
			{"label": _("Reference"), "items": ["Journal Entry"]},
		],
	}
