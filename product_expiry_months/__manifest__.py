# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Expiration of products in months',
    'summary': """
        Odoo uses days to monitor batches in stock products.
        With this module you can manage the expiration times 
        of the products in months instead of days.""",

    'author': 'Calyx Servicios S.A., Odoo Community Association (OCA)',
    'maintainers': ['Milton Guzman'],

    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/11.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '11.0.1.0.0',
    # see https://odoo-community.org/page/development-status
    'development_status': 'Production/Stable',

    'application': False,
    'installable': True,

    # any module necessary for this one to work correctly
    'depends': ['base', 'product_expiry'],

    # always loaded
    'data': [
        'views/product_template_views.xml',
    ],
}
