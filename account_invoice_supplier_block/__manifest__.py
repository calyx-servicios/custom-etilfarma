# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Supplier Block",
    "summary": """
        This module blocks supplier switching if origin is set.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["LucasSoto"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Invoicing",
    "version": "11.0.0.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "depends": [
        "account",
        "account_invoicing"
    ],
    "data": [
        "views/account_invoice_view.xml",
    ],
}
