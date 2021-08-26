# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class ProductionDispatch(models.Model):
    _name = 'stock.production.dispatch'
    _inherit = ['mail.thread']
    _description = 'Import Dispatch'

    name = fields.Char(
        'Import Dispatch',
        required=True, help="Unique Import Dispatch")
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

    _sql_constraints = [
        ('name_ref_uniq', 'Check(1=1)',
         'The combination of serial number and product must be unique !'),
    ]

    @api.model
    def create(self, vals):
        active_picking_id = self.env.context.get('active_picking_id', False)
        if active_picking_id:
            picking_id = self.env['stock.picking'].browse(active_picking_id)
            if picking_id and not picking_id.picking_type_id.use_create_lots:
                raise UserError(
                    _("You are not allowed to create a lot for this picking type"))
        return super(ProductionDispatch, self).create(vals)

    @api.multi
    def write(self, vals):
        if 'product_id' in vals:
            move_lines = self.env['stock.move.line'].search(
                [('dispatch_id', 'in', self.ids), ('product_id', '!=', vals['product_id'])])
            if move_lines:
                raise UserError(_(
                    'You are not allowed to change the product linked to a serial or lot number '
                    + 'if some stock moves have already been created with that number. '
                    + 'This would lead to inconsistencies in your stock.'
                ))
        return super(ProductionDispatch, self).write(vals)