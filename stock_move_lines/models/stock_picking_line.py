from odoo import fields, models

class StockPickingType(models.Model):
    _inherit = "stock.picking.type"

    def get_stock_move_line_action(self):
        action = self.env.ref('stock.stock_move_line_action').read()[0]
        if self.code == 'incoming':
            action['context'] = {
                'is_reception':True,
            }
        if self.code == 'outgoing':
            action['context'] = {
                'is_reception':False,
            }
        action['domain'] = [('picking_type_code', '=', self.code)]
        return action