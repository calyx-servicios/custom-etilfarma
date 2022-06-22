from odoo import models

class StockBackorderConfirmation(models.TransientModel):
    _inherit = 'stock.backorder.confirmation'

    def process(self):
        ret = super(StockBackorderConfirmation, self).process()
        pickings = self.env['stock.picking'].search([('origin','=',self.pick_ids.origin),('id','>',self.pick_ids.id)])
        for picking in pickings:
            picking.do_unreserve()
        return ret 