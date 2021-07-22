from odoo import models, fields


class StockChangeProductQty(models.TransientModel):

    _inherit = 'stock.change.product.qty'

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )
