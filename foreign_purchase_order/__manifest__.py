# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Foreign Purchase Order",
    "summary": """
        This module add a page in purchase order for the foreign fields.
        Besides, add an if statement in the validation of the document\n
        number in purchase invoice.
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM", "LucasSoto"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "11.0.3.1.4",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "base",
        "purchase",
        "purchase_order_types",
        "stock",
        "l10n_ar_account",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "views/stock_view.xml",
        "views/purchase_packaging_view.xml",
        "views/purchase_dispatcher_view.xml",
        "views/purchase_packing_list_view.xml",
        "views/purchase_delivery_chanel_view.xml",
        "views/purchase_booking_conveyance_view.xml",
        "views/purchase_place_delivery_view.xml",
        "views/purchase_shipment_view.xml",
        "views/purchase_certificate_of_analysis_view.xml",
        "views/purchase_import_license_view.xml",
        "views/res_config_settings_views.xml",
        "views/product_product_view.xml",
    ],
}
