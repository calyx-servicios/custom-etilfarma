# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Foreign Purchase Order Alerts",
    "summary": """
        This module add "alerts" in purchase order tree view.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM", "FedericoGregori"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "11.0.1.0.1",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": [
        "web_tree_dynamic_colored_field",
        "purchase_order_types",
        "foreign_purchase_order",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
}
