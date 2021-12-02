# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase lines in wait",
    "summary": """
        shows a tree view of the product lines in the waiting state""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Andres Andrade"],
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
        "stock_voucher",
        "foreign_trade",
        "purchase_order_invoice_to",
        "stock_move_lines",
        "purchase",
        "stock_move_lines",
        ],
    "data": [
        "views/stock_picking_view.xml",
        "views/menuitem.xml",
        ],
}
