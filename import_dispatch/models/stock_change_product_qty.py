from odoo import models, fields, _, tools


class StockChangeProductQty(models.TransientModel):

    _inherit = 'stock.change.product.qty'

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )
    dispatch_name = fields.Char()
    lot_name = fields.Char()
    type_update = fields.Selection([
        ("update", "Update"),
        ("new_lot", "New Lot"),
        ("new_dispatch", "New Dispatch")]
        ,default="update")
    life_date = fields.Datetime(
        string='End of Life Date',
        help='This is the date on which the goods with this Serial Number may '
             'become dangerous and must not be consumed.',
    )

    def change_product_qty(self):
        """ Changes the Product Quantity by making a Physical Inventory. """
        Inventory = self.env['stock.inventory']
        for wizard in self:
            product = wizard.product_id.with_context(location=wizard.location_id.id, lot_id=wizard.lot_id.id)
            lot_id = self.env['stock.production.lot'].search([('dispatch_id.name','=',wizard.dispatch_id.name),('name','=',wizard.lot_id.name)])
            if wizard.type_update == "update":
                lot_id = self.env['stock.production.lot'].search([('dispatch_id.name','=',wizard.dispatch_id.name),('name','=',wizard.lot_id.name),('product_id','=',wizard.product_id.id)])
                wizard.dispatch_id.product_qty = wizard.new_quantity
                self.lot_id = lot_id
            if wizard.type_update == "new_lot":
                dispatch_id = self.env['stock.production.dispatch'].create({
                        'name': wizard.dispatch_name,
                        'product_id': wizard.product_id.id,
                        'product_qty':wizard.new_quantity,
                    })
                lot_id = self.env['stock.production.lot'].create({
                        'name': wizard.lot_name,
                        'product_id': wizard.product_id.id,
                        'product_qty':wizard.new_quantity,
                        'dispatch_id':dispatch_id.id,
                        'life_date':wizard.life_date,
                    })
                self.lot_id = lot_id
            if wizard.type_update == "new_dispatch":
                dispatch_id = self.env['stock.production.dispatch'].create({
                        'name': wizard.dispatch_name,
                        'product_id': wizard.product_id.id,
                        'product_qty':wizard.new_quantity,
                    })
                lot_id = self.env['stock.production.lot'].create({
                        'name': wizard.lot_id.name,
                        'product_id': wizard.product_id.id,
                        'product_qty':wizard.new_quantity,
                        'dispatch_id':dispatch_id.id,
                        'life_date':wizard.lot_id.life_date,
                    })
                self.lot_id = lot_id
            if wizard.product_id.id and lot_id.id:
                inventory_filter = 'none'
            elif wizard.product_id.id:
                inventory_filter = 'product'
            else:
                inventory_filter = 'none'
            line_data = wizard._action_start_line()
            inventory = Inventory.create({
                'name': _('INV: %s') % tools.ustr(wizard.product_id.display_name),
                'filter': inventory_filter,
                'product_id': wizard.product_id.id,
                'location_id': wizard.location_id.id,
                'lot_id': lot_id.id,
                'line_ids': [(0, 0, line_data)],
            })
            inventory.action_done()
        return {'type': 'ir.actions.act_window_close'}


class StockQuant(models.Model):
    _inherit = 'stock.quant'
    
    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
        related='lot_id.dispatch_id'
    )