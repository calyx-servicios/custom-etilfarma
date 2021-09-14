# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Foreign Report",
    "summary": """
        New purchase custom report""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["marcooegg"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Report",
    "version": "11.0.1.1.3",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": [
        "purchase",
        "purchase_order_types",
        "foreign_purchase_order",
        "foreign_purchase_lines",
        "purchase_order_marks",
    ],
    "data": [
        "security/ir.model.access.csv",
        "view/purchase_order_view.xml",
        "view/report_config_parameter.xml",
        "report/purchase_order_foreign_template.xml",
        "report/purchase_order_foreign_report.xml",
        "data/mail_template_data.xml",
        "data/mail_template_data_impo.xml",
        "data/report_header_parameters.xml",
    ],
}
