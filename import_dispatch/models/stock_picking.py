# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    line_dispatch_name = fields.Char(
        string='Dispatch Name',
    )

    @api.multi
    def button_validate(self):
        if self.picking_type_code == 'incoming':
            for move in self.move_line_ids:
                dispatch = self.env['stock.production.dispatch'].search([('name','=',move.dispatch_name),('product_id','=', move.product_id.id)])
                if not dispatch:
                    rec = self.env['stock.production.dispatch'].create({
                        'name': move.dispatch_name,
                        'product_id': move.product_id.id,
                        'product_uom_id':move.product_uom_id.id,
                        'product_qty':move.qty_done,
                    })
                else:
                    dispatch.write({'product_qty': dispatch.product_qty + move.qty_done})           
        
        if self.picking_type_code == 'outgoing':                   
            for move in self.move_line_ids:
                dispatch = self.env['stock.production.dispatch'].search([('name','=',move.dispatch_name),('product_id','=', move.product_id.id)])
                if dispatch:
                    dispatch.write({'product_qty': dispatch.product_qty - move.qty_done})

        res = super(StockPicking, self).button_validate() 
        return res             
            
