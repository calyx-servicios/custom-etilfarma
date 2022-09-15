# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Purchase Order Bulk Edit",
    "summary": """
        Adding mass edit wizard by date.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DeykerGil"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Purchase",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["purchase"],
    "data": [
        "wizard/purchase_order_bulk_edit.xml",
    ],
}
