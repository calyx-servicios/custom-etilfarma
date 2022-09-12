# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Partner Hyperlink",
    "summary": """
        Add hyperlink to the partner_id field 
        within a delivery order.""",
    "author": "Calyx Servicios S.A.",
    "maintainers": ["DeykerGil"],
    "website": "http://odoo.calyx-cloud.com.ar/",
    "license": "AGPL-3",
    "category": "Inventory",
    "version": "11.0.1.0.0",
    "development_status": "Production/Stable",
    "application": False,
    "installable": True,
    "external_dependencies": {
        "python": [],
        "bin": [],
    },
    "depends": ["stock"],
    "data": [
        "views/stock_picking.xml"
    ],
}
