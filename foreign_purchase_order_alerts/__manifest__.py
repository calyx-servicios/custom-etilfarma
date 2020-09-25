# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Foreign Purchase Order Alerts',
    'summary': """
        Summary of the module's purpose""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['<Github/Gitlab Username/s>'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Technical Settings',
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
        'web_tree_dynamic_colored_field',
        'foreign_purchase_order'
    ],

    # always loaded
    'data': [
        'views/purchase_order_view.xml',
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
