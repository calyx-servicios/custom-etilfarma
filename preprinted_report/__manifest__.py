# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Preprinted report",
    "summary": """
        Preprinted report""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DarwinAndrade"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Report",
    "version": "11.0.1.1.3",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {"python": ["num2words"], "bin": []},
    "depends": [
        "l10n_ar_afipws_fe",
        "l10n_ar_aeroo_einvoice",
        "l10n_ar_aeroo_stock",
        "foreign_trade"
    ],
    "data": [
        "views/stock_picking_view.xml",
        "report/invoice_report.xml",
    ],
}
