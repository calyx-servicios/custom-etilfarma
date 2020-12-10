# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Einvoice custom Output",
    "summary": """
        Custom Output in einvoice""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["JhoneM"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Report",
    "version": "11.0.1.1.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": [], "bin": []},
    "depends": ["l10n_ar_afipws_fe", "l10n_ar_aeroo_einvoice"],
    "data": ["report/invoice_report.xml"],
}
