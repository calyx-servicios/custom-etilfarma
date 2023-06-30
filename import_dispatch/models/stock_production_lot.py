from odoo import models, fields,api, _
from odoo.exceptions import UserError, ValidationError


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )

    @api.model
    def create(self, vals):
        dispatch = self.env['stock.production.dispatch'].search([('id','=',vals.get("dispatch_id",False))])
        lot_ids = self.env['stock.production.lot'].search([
            ('name','=',vals.get("name",False)),
            ('product_id','=',vals.get("product_id",False)),
            ])
        for lot_id in lot_ids:
            if lot_id.dispatch_id.name and lot_id.dispatch_id.name == dispatch.name:
                raise ValidationError(_('The combination of serial number and product must be unique !'))
        return super(StockProductionLot, self).create(vals)

    _sql_constraints = [
        ('name_ref_uniq', 'Check(1=1)', 'The combination of serial number and product must be unique !'),
    ]
