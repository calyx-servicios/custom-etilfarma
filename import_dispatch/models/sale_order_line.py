# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    line_dispatch_name = fields.Many2one('stock.production.dispatch',
        string='Dispatch Name',
        # related='lot_id.dispatch_id'
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
            dispatch_ids = self.env["stock.production.dispatch"].search([("product_id", "=", self.product_id.id)])
            for dispatch_id in dispatch_ids:
                if dispatch_id.name not in names:
                    #  and dispatch_id.lot_id.id == self.loot_name.dispatch_id.id
                    filter_ids.append(dispatch_id.id)
                    names.append(dispatch_id.name)

            self.dispatch_filter = [(6,0, filter_ids)]

    dispatch_filter = fields.Many2many(
        'stock.production.lot')