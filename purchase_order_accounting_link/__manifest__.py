# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Purchase Orders from Accounting App',
    'summary': """
        This module adds the functionality to create Purchase Orders from the Account App.""",

    'author': 'Calyx Servicios S.A.',
    'maintainers': ['FedericoGregori', 'JhoneM'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '11.0.1.0.1',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },

    # any module necessary for this one to work correctly
    'depends': ['account', 'purchase', 'purchase_order_types'],

    # always loaded
    'data': [
        'views/account_invoice_view.xml',
        'views/purchase_order_view.xml'
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
