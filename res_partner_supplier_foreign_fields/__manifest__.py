# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Supplier Purchase Foreign Fields",
    "summary": """
        This module allows to you configurate the foreign
        fields required for every partner.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Lolstalgia"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["base", "purchase", "foreign_purchase_order"],
    "data": ["views/res_partner_view.xml"],
}
