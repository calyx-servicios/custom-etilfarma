# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Control Validate Invoice",
    "summary": """
        Add new fields to the product module.
    """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["carlamiquetan"],
    "website": "https://odoo.calyx-cloud.com.ar/",
    "category": "Technical Settings",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["stock"],
    'data': [
         'views/product_logistics_form_view.xml',
    ],
}