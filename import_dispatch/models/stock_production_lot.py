##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, fields,api, _
from odoo.exceptions import UserError

class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )

    _sql_constraints = [
        ('name_ref_uniq',  'Check(1=1)', 'The combination of serial number and product must be unique !'),
    ]

    @api.model
    def create(self, vals):
        records = self.env['stock.production.lot'].search([
                    ('product_id','=',vals['product_id'])])
        for record in records:
            if record.dispatch_id.id == vals.get('dispatch_id',self.dispatch_id.id) and record.name == vals['name']:
                raise UserError(
                    _("The combination of serial number, product and dispatch number must be unique"))
        return super(StockProductionLot, self).create(vals)

    @api.multi
    def write(self, vals):
        records = self.env['stock.production.lot'].search([
                    ('product_id','=',vals.get('product_id',self.product_id.id))])
        for record in records:
            if record.dispatch_id.id == vals.get('dispatch_id',self.dispatch_id.id) and record.name == vals.get('name',self.name):
                raise UserError(
                    _("The combination of serial number, product and dispatch number must be unique"))
        return super(StockProductionLot, self).write(vals)