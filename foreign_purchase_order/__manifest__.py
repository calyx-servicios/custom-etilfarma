# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Foreign Purchase Order",
    "summary": """
        This module add a page in purchase order for the foreign fields.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Lolstalgia", "LucasSoto"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    "category": "Purchase",
    "version": "11.0.3.0.1",
    # see https://odoo-community.org/page/development-status
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    # any module necessary for this one to work correctly
    "depends": ["base", "purchase", "purchase_order_types", "stock"],
    # always loaded
    "data": [
        "security/ir.model.access.csv",
        "views/purchase_order_view.xml",
        "views/purchase_packaging_view.xml",
        "views/purchase_packing_list_view.xml",
        "views/purchase_delivery_chanel_view.xml",
        "views/purchase_booking_conveyance_view.xml",
        "views/purchase_place_delivery_view.xml",
        "views/purchase_shipment_view.xml",
        "views/purchase_certificate_of_analysis_view.xml",
        "views/purchase_import_license_view.xml",
        "views/res_config_settings_views.xml",
        "views/product_product_view.xml"
    ],
}
