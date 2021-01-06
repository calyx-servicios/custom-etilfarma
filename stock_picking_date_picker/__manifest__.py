# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Inventory Date Picker",
    "summary": """
        Add new 'date picker' field in inventory.
        Hide fields in inventory purchase view.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Inventory",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["stock", "foreign_purchase_order"],
    "data": ["views/stock_picking.xml"],
}
