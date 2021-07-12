# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Import Dispatch",
    "summary": """
        Creates "Import Dispatch" within the product base, 
        with the same batch logic.""",
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
    "depends": [
        "l10n_ar_stock",
        "stock",
        "foreign_purchase_order",
        "foreign_trade",
        "purchase",
        "stock_move_lines"
        ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_production_dispatch_views.xml",
        "views/stock_move_line_views.xml",
        "views/stock_picking_views.xml",
        "views/sale_order_views.xml",
        ],
}
