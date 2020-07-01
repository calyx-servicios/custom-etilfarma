# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Purchase Order Line Hide Date Planned",
    "summary": """
        This module changes the default behaviour to make the Purchase Order
        'Scheduled Date' apply to the entire order.""",
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
        "purchase"
    ],
    "data": [
        "views/purchase_order_view.xml"
    ],
}
