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
        "stock",
        "foreign_purchase_order",
        "foreign_trade",
        "purchase",
        "stock_move_lines",
        "l10n_ar_stock",
        ],
    "data": [
        "security/ir.model.access.csv",
        "views/stock_production_dispatch_views.xml",
        "views/stock_move_line_views.xml",
        "views/sale_order_views.xml",
        "views/stock_production_lot_view.xml",
        "views/stock_change_product_views.xml",
        ],
}
