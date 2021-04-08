# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Chanel",
    "summary": """
        Add a "Chanel" field in the Purchase Request""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Custom",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["purchase"],
    "data": ["views/purchase_order_view.xml", 
             "views/purchase_order_chanel_view.xml",
             "security/ir.model.access.csv"],
}
