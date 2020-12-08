# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Purchase Order Types',
    'summary': """
        This module add the option to assing a type to the Purchase Order.""",

    'author': 'Calyx Servicios S.A.',
    'maintainers': ['FedericoGregori'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchases',
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    'application': False,
    'installable': True,
    'external_dependencies': {
        'python': [],
        'bin': [],
    },

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'purchase'
        ],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/account_payment_term.xml',
        'data/purchase_order_type.xml',
        'views/res_partner_view.xml',
        'views/purchase_order_view.xml',
        'views/purchase_order_type_view.xml',
        'views/ir_sequence_view.xml'
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
