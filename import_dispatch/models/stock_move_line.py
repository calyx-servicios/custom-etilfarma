# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError
from openerp.tools.translate import _

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )
    dispatch_name = fields.Char(
        string='Dispatch Name',
    )
    life_date = fields.Date(
        string='Life Date',
    )
    lot_id = fields.Many2one(
        string='lote prueba'
    )
    @api.onchange('lot_name')
    def onchange_document_number(self):
        for rec in self.picking_id.move_lines:
            if self.product_id.id == rec.product_id.id and rec.dispatch_name and not self.dispatch_name:
                self.dispatch_name = rec.dispatch_name

    @api.onchange('dispatch_id')
    def onchange_dispatch_id(self):
        self.life_date = self.dispatch_id.lot_id.life_date
        
    @api.onchange("product_id")
    def _get_lot_by_product(self):
        names = []
        filter_ids = []
        lot_ids = self.env["stock.production.lot"].search([("product_id", "=", self.product_id.id)])
        for lot_id in lot_ids:
            if lot_id.name not in names:
                filter_ids.append(lot_id.id)
                names.append(lot_id.name)
                    
        self.lot_filter = [(6,0, filter_ids)]

    lot_filter = fields.Many2many(
        'stock.production.lot')
        
    @api.onchange("lot_id")
    def _get_dispatch_by_product(self):
        names = []
        filter_ids = []
        for rec in self:
            if rec.lot_id:
                dispatch_ids = self.env["stock.production.dispatch"].search([("product_id", "=", rec.product_id.id),("lot_id", "=", rec.lot_id.id)])
                lot_ids = self.env["stock.production.lot"].search([("product_id", "=", rec.product_id.id),("name", "=", rec.lot_id.name)])
                for dispatch_id in dispatch_ids:
                    for lot_id in lot_ids:
                        if dispatch_id.id == lot_id.dispatch_id.id: 
                            if dispatch_id.name not in names:
                                filter_ids.append(dispatch_id.id)
                                names.append(dispatch_id.name)
                    
                    
            rec.dispatch_filter = [(6,0, filter_ids)]

    dispatch_filter = fields.Many2many(
        'stock.production.lot')
