# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Foreign Purchase Lines",
    "summary": """
        This module add new fields in purchase order lines""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "11.0.1.0.1",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "base",
        "purchase",
        "purchase_order_types",
        "foreign_purchase_order",
        "web_notify",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "views/product_template_view.xml",
        "views/product_attribute_view.xml",
        "views/product_attribute_value_view.xml",
    ],
}
