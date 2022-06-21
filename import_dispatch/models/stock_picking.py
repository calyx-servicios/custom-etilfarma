# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError, ValidationError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    line_dispatch_name = fields.Char(
        string='Dispatch Name',
    )

    @api.multi
    def button_validate(self):
        res = super(StockPicking, self).button_validate() 
        if self.picking_type_code == 'incoming':
            for move in self.move_line_ids:
                rec = self.env['stock.production.dispatch'].create({
                    'name': move.dispatch_name,
                    'product_id': move.product_id.id,
                    'product_uom_id':move.product_uom_id.id,
                    'product_qty':move.qty_done,
                })
                lot_ids = self.env['stock.production.lot'].search([
                    ('name','=',move.lot_name),
                    ('product_id','=', move.product_id.id)
                ])
                for lot_id in lot_ids:
                    if lot_id.dispatch_id.name == move.dispatch_name:
                        raise ValidationError(_('The combination of serial number and product must be unique !'))               
                lot_name =  self.env['stock.production.lot'].search([('name','=',move.lot_name),('product_id','=', move.product_id.id),('dispatch_id','=', False)],limit=1)
                if not lot_name:
                    lot_name = self.env['stock.production.lot'].create({
                    'name': move.lot_name,
                    'product_id': move.product_id.id,
                    'product_uom_id':move.product_uom_id.id,
                    'product_qty':move.qty_done,
                    'dispatch_id': rec.id,
                    'life_date': move.move_id.editable_life_date,
                    })
                else:
                    lot_name.write({
                        'dispatch_id': rec.id,
                        'life_date': move.move_id.editable_life_date,
                    })        
                move.dispatch_id = rec.id
                move.lot_id = lot_name.id
                
        if self.picking_type_code == 'outgoing':
            for move in self.move_lines:
                dispatch = self.env['stock.production.dispatch'].search([('name','=',move.dispatch_name),('product_id','=', move.product_id.id)])
                if dispatch:
                    dispatch.write({'product_qty': dispatch.product_qty - move.qty_done})

        return res             
            
