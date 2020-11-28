# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Unified Menu Purchase Orders - Except IMA/OTC Orders',
    'summary': """
        The purpose of this module is to remove Request for Quotation Menu and show all 
        Purchase Orders in a unique menu item.
        IMA/OTC Orders maintain other menu item""",

    'author': 'Calyx Servicios S.A.',
    'maintainers': ['FedericoGregori'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Purchase',
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
    'depends': ['purchase', 'purchase_order_invoice_to','purchase_order_accounting_link'],

    # always loaded
    'data': [
        'views/purchase_order_view.xml',
        #     'views/views.xml',
        #     'views/templates.xml',
    ],

    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
}
