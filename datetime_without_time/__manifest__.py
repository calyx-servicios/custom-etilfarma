{
    "name": "Datetime Without Time",
    "version": "11.0.1",
    "category": "Tools",
    "author": "Calyx",
    "website": "www.calyxservicios.com.ar",
    "license": "AGPL-3",
    "summary": """Change all datetime fields to date only in the following views:
                views/purchase_order_view.xml
                views/purchase_request_view.xml
                views/sale_order_view.xml
                views/stock_inventory_view.xml
                views/stock_move_line_view.xml
                views/stock_picking_view.xml
                views/stock_production_lot_view.xml
                views/stock_quant_view.xml""",
    "depends": [
        "sale",
        "purchase_request",
        "purchase",
        "stock",
        "foreign_purchase_lines",
    ],
    "external_dependencies": {},
    "data": [
        "views/purchase_order_view.xml",
        "views/purchase_request_view.xml",
        "views/sale_order_view.xml",
        "views/stock_inventory_view.xml",
        "views/stock_move_line_view.xml",
        "views/stock_picking_view.xml",
        "views/stock_production_lot_view.xml",
        "views/stock_quant_view.xml",
    ],
    "demo": [],
    "test": [],
    "installable": True,
    "auto_install": False,
    "application": False,
}
