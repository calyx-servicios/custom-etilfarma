# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    "name": "Customer field crm",
    "summary": """
        """,
    "author": "Calyx Servicios S.A.",
    "maintainers": ["Andres Andrade"],
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
    'depends': [
        'base_setup',
        'sales_team',
        'mail',
        'calendar',
        'resource',
        'fetchmail',
        'utm',
        'web_planner',
        'web_tour',
        'contacts'
    ],
    "data": [
        "views/crm_lead_views.xml",
        ],
}
