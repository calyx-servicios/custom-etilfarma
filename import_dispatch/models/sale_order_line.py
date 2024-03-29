from odoo import api, fields, models, _

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    line_dispatch_name = fields.Many2one('stock.production.dispatch',
        string='Dispatch Name'
    )

    @api.onchange("product_id")
    def _get_lot_by_product(self):
        names = []
        filter_ids = []
        lot_ids = self.env["stock.production.lot"].search([("product_id", "=", self.product_id.id)])
        for lot_id in lot_ids:
            if lot_id.name not in names and lot_id.product_qty > 0:
                filter_ids.append(lot_id.id)
                names.append(lot_id.name)

        self.lot_filter = [(6, 0, filter_ids)]

    @api.depends('loot_name')
    def _get_dispatch_by_product(self):
        for rec in self:
            names = []
            filter_ids = []
            if rec.loot_name:
                dispatch_ids = self.env["stock.production.dispatch"].search([
                    ("product_id", "=", rec.product_id.id),
                    ("lot_id", "=", rec.loot_name.id)
                ])
                lot_ids = self.env["stock.production.lot"].search([
                    ("product_id", "=", rec.product_id.id),
                    ("name", "=", rec.loot_name.name)
                ])
                for dispatch_id in dispatch_ids:
                    for lot_id in lot_ids:
                        if dispatch_id.id == lot_id.dispatch_id.id and lot_id.product_qty > 0:
                            if dispatch_id.name not in names:
                                filter_ids.append(dispatch_id.id)
                                names.append(dispatch_id.name)
            rec.write({'dispatch_filter': [(6, 0, filter_ids)]})

