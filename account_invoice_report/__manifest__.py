# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Account Invoice Report",
    "summary": """
        Add templates to accounting""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Report",
    "version": "11.0.1.1.3",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "account",
    ],
    "data": [
        "data/mail_template_data.xml",
        "data/mail_template_data_impo.xml",
        "report/invoice_report.xml",
    ],
}
