from odoo import models, fields,api, _
from odoo.exceptions import UserError, ValidationError

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )

    @api.model
    def create(self, vals):
        lot_id = self.env['stock.production.lot'].search([
            ('dispatch_id','=',vals.get("dispatch_id.id",self.dispatch_id.id)),
            ('name','=',vals.get("name",self.name)),
            ('product_id','=',vals.get("product_id.id",self.product_id.id)),
            ])        
        if len(lot_id.ids)>0:
            raise ValidationError('The combination of serial number and product must be unique !')
        return super(StockProductionLot, self).create(vals)

    @api.multi
    def write(self, vals):
        lot_id = self.env['stock.production.lot'].search([
            ('dispatch_id.name','=',vals.get("dispatch_id.name",self.dispatch_id.name)),
            ('name','=',vals.get("name",self.name)),
            ('product_id','=',vals.get("product_id.id",self.product_id.id)),
            ])
        if len(lot_id.ids)>1:
            raise ValidationError('The combination of serial number and product must be unique !')
        return super(StockProductionLot, self).write(vals)
    
    _sql_constraints = [
        ('name_ref_uniq', 'Check(1=1)', 'The combination of serial number and product must be unique !'),
    ]
