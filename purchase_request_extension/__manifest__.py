# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Request Extension",
    "summary": """
        This module extends and modifies the Purchase Request functions.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["LucasSoto"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchases",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "purchase_request",
        "purchase_order_types",
        "purchase_order_invoice_to"
    ],
    "data": [
        "views/purchase_request_view.xml",
        "wizard/purchase_request_line_make_purchase_order_view.xml"
    ],
}
