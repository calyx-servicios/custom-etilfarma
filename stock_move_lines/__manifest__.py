# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Stock Moves",
    "summary": """
        Add within inventories (on delivery and receipt) 
        a tree view per product line""",
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
        "stock_voucher",
        "purchase_order_invoice_to"
        "purchase_order_types",
        "foreign_trade"
        ],
    "data": [
        "views/stock_move_line_view.xml",
        "views/stock_picking_type_view.xml",
        "views/sale_order_line_view.xml",
        ],
}
