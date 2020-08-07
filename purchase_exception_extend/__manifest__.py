# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Exception Extend",
    "summary": """
        Add purchase exceptions""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Lolstalgia"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "base",
        "purchase_exception",
        "foreign_purchase_order",
        "purchase_order_invoice_to",
    ],
    "data": [
        "data/exception_rule_data.xml",
        "views/purchase_exception_views.xml",
    ],
}
