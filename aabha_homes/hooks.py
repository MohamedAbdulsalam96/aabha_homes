app_name = "aabha_homes"
app_title = "Aabha Homes"
app_publisher = "sammish"
app_description = "Building Homes"
app_email = "sammish.thundiyil@gmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/aabha_homes/css/aabha_homes.css"
# app_include_js = "/assets/aabha_homes/js/aabha_homes.js"

# include js, css files in header of web template
# web_include_css = "/assets/aabha_homes/css/aabha_homes.css"
# web_include_js = "/assets/aabha_homes/js/aabha_homes.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "aabha_homes/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
doctype_js = {"Material Request" : "public/js/material_request.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "aabha_homes/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
#	"methods": "aabha_homes.utils.jinja_methods",
#	"filters": "aabha_homes.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "aabha_homes.install.before_install"
# after_install = "aabha_homes.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "aabha_homes.uninstall.before_uninstall"
# after_uninstall = "aabha_homes.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "aabha_homes.utils.before_app_install"
# after_app_install = "aabha_homes.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "aabha_homes.utils.before_app_uninstall"
# after_app_uninstall = "aabha_homes.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "aabha_homes.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
#	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
#	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
#	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
#     "Journal Entry": {
#         "on_cancel": "aabha_homes.aabha_homes.utils.validate_je_cancel"
#     }
# }
#	"*": {
#		"on_update": "method",
#		"on_cancel": "method",
#		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
#	"all": [
#		"aabha_homes.tasks.all"
#	],
#	"daily": [
#		"aabha_homes.tasks.daily"
#	],
#	"hourly": [
#		"aabha_homes.tasks.hourly"
#	],
#	"weekly": [
#		"aabha_homes.tasks.weekly"
#	],
#	"monthly": [
#		"aabha_homes.tasks.monthly"
#	],
# }

# Testing
# -------

# before_tests = "aabha_homes.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
#	"frappe.desk.doctype.event.event.get_events": "aabha_homes.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
#	"Task": "aabha_homes.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["aabha_homes.utils.before_request"]
# after_request = ["aabha_homes.utils.after_request"]

# Job Events
# ----------
# before_job = ["aabha_homes.utils.before_job"]
# after_job = ["aabha_homes.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
#	{
#		"doctype": "{doctype_1}",
#		"filter_by": "{filter_by}",
#		"redact_fields": ["{field_1}", "{field_2}"],
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_2}",
#		"filter_by": "{filter_by}",
#		"partial": 1,
#	},
#	{
#		"doctype": "{doctype_3}",
#		"strict": False,
#	},
#	{
#		"doctype": "{doctype_4}"
#	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
#	"aabha_homes.auth.validate"
# ]
fixtures = [
    {
        "doctype": "Custom Field",
        "filters": [
            [
                "name",
                "in",
                [
                    "Employee-custom_is_supervisor",
                    "Employee-custom_is_worker",
                    "Employee-custom_employee_state",
                    "Stock Entry-custom_material_consumption_entry",
                    "Employee-petty_cash_account",
                    "Journal Entry-petty_cash_request",
                    "Material Request-custom_site_supervisor",
                    "Material Request-custom_cost_center"
                ]
            ]
        ]
    }
]