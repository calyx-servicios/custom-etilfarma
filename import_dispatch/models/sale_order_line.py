# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

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
                if lot_id.name not in names:
                    filter_ids.append(lot_id.id)
                    names.append(lot_id.name)

            self.lot_filter = [(6,0, filter_ids)]

    lot_filter = fields.Many2many(
        'stock.production.lot')

    @api.onchange("loot_name")
    def _get_dispatch_by_product(self):
        names = []
        filter_ids = []
        for rec in self:
            if rec.loot_name:
                # import wdb
                # wdb.set_trace()
                dispatch_ids = self.env["stock.production.dispatch"].search([("product_id", "=", rec.product_id.id),("lot_id", "=", rec.loot_name.id)])
                lot_ids = self.env["stock.production.lot"].search([("product_id", "=", rec.product_id.id),("name", "=", rec.loot_name.name)])
                for dispatch_id in dispatch_ids:
                    for lot_id in lot_ids:
                        if dispatch_id.id == lot_id.dispatch_id.id: 
                            if dispatch_id.name not in names:
                                filter_ids.append(dispatch_id.id)
                                names.append(dispatch_id.name)
                    
                    
            rec.dispatch_filter = [(6,0, filter_ids)]

    dispatch_filter = fields.Many2many(
        'stock.production.lot')