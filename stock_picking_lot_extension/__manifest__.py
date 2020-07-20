# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
{
    'name': 'Stock Picking Lot Extension',
    'summary': "Adds lot's life_date field on several tree views",
    'author': 'Calyx Servicios S.A.',
    'maintainers': ['LucasSoto'],
    'website': 'http://odoo.calyx-cloud.com.ar/',
    'license': 'AGPL-3',
    'category': 'Inventory',
    'version': '11.0.1.0.0',
    'development_status': 'Production/Stable',
    'application': False,
    'installable': True,
    'depends': [
        'product_expiry',
        'stock_move_quick_lot'
    ],
    'data': [
        'views/stock_view.xml',
    ],
}
