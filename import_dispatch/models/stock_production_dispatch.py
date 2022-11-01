# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class ProductionDispatch(models.Model):
    _name = 'stock.production.dispatch'
    _inherit = ['mail.thread']
    _description = 'Import Dispatch'

    def _compute_lot_id(self):
        lot_id = self.env['stock.production.lot'].search([('dispatch_id.name','=',self.name),('product_id.id','=',self.product_id.id)],limit=1)
        self.lot_id = lot_id 
    
    name = fields.Char(
        'Import Dispatch',
         help="Unique Import Dispatch")
    ref = fields.Char('Internal Reference')
    product_id = fields.Many2one(
        'product.product', 'Product',
        domain=[('type', 'in', ['product', 'consu'])], required=True)
    product_uom_id = fields.Many2one(
        'product.uom', 'Unit of Measure',
        related='product_id.uom_id', store=True)
    quant_ids = fields.One2many(
        'stock.quant', 'lot_id', 'Quants', readonly=True)
    create_date = fields.Datetime('Creation Date')
    product_qty = fields.Float('Quantity')
    lot_id = fields.Many2one(
        'stock.production.lot',
        compute='_compute_lot_id') 

    _sql_constraints = [
        ('name_ref_uniq', 'unique(1=1)', 'Dispatch must be unique!'),
    ]