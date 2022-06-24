{
    "name": "Foreign Purchase Order Custom",
    "summary": """
    This module modifies fields and views in the delivery order
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "base",
        "purchase",
        "purchase_order_types",
        "stock",
        "l10n_ar_account",
        "foreign_purchase_order",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
}
