# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Purchase Order Invoice To',
    'summary': """
        This module add the option to assing a Client as Buyer in PO's.""",

    'author': 'Calyx Servicios S.A.',
    'maintainers': ['FedericoGregori'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchases',
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
    'depends': [
        'base',
        'purchase',
        'purchase_order_types',
        'foreign_purchase_order',
        'l10n_ar_account'
        ],

    'data': [
        'security/ir.model.access.csv',
        'data/ir_sequence.xml',
        'data/purchase_order_type.xml',
        'views/purchase_order_view.xml',
        'views/partner_oct_view.xml'
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
