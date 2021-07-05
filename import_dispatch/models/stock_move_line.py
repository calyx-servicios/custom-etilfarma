# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

class StockMoveLine(models.Model):
    _inherit = "stock.move.line"

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )
    dispatch_name = fields.Char(
        string='Dispatch Name',
    )
    @api.onchange('lot_name')
    def onchange_document_number(self):
        for rec in self.picking_id.move_lines:
            if self.product_id.id == rec.product_id.id and rec.dispatch_name and not self.dispatch_name:
                self.dispatch_name = rec.dispatch_name
