from frappe import _

def get_data():
	return {
		"fieldname": "material_consumption_entry",
		"non_standard_fieldnames": {
			"Stock Entry": "custom_material_consumption_entry",
		},
		"transactions": [
			{"label": _("Stock Entry"), "items": ["Stock Entry"]},
		],
	}