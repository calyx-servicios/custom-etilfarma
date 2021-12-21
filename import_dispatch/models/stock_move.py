# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _compute_line_dispatch_name(self):
        for lines in self:
            name = []
            name_id = []
            for line in lines.move_line_ids:
                name.append(line.dispatch_name)
                name_id.append(line.dispatch_id.name)
            if len(name)>0:
                if name[0]:
                    lines.line_dispatch_name = ','.join(name)
                else:
                    lines.line_dispatch_name = ""
            if len(name_id)>0 and lines.line_dispatch_name == "":
                if name_id[0]:
                    lines.line_dispatch_name = ','.join(name_id)
                else:
                    lines.line_dispatch_name = ""

    @api.multi
    def _compute_life_date(self):
        for lines in self:
            name = []
            for line in lines.move_line_ids:
                name.append(line.life_date)
            if len(name)>0:
                if name[0]:
                    lines.editable_life_date = ','.join(name)
                else:
                    lines.editable_life_date = ""

    @api.multi
    def _compute_lot_name(self):
        for lines in self:
            name = []
            for line in lines.move_line_ids:
                name.append(line.lot_name)
            if len(name)>0:
                if name[0]:
                    lines.line_lot_name = ','.join(name)
                else:
                    lines.line_lot_name = ""
    
    # @api.multi
    # def _compute_lot_name(self):
    #     for lines in self:
    #         name = []
    #         for line in lines.move_line_ids:
    #             name.append(line.loot_name)
    #         if len(name)>0:
    #             if name[0]:
    #                 lines.line_lot_name = ','.join(name)
    #             else:
    #                 lines.line_lot_name = ""
                    
    line_dispatch_name = fields.Char(
        string='Dispatch Name',
        compute="_compute_line_dispatch_name",
    )

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )

    dispatch_name = fields.Char(
        string='Dispatch Name',
    )
    line_lot_name = fields.Char(
        string='Lot Name',
        compute="_compute_lot_name",
    )
    editable_life_date = fields.Date(
        string='End of Life Date',
        compute="_compute_life_date",
        help='This is the date on which the goods with this Serial Number may '
             'become dangerous and must not be consumed.',
    )
    
    @api.multi
    def production_lot_from_name(self, create_lot=True):
        StockProductionLot = self.env['stock.production.lot']
        if not self.line_lot_name:
            if self.move_line_ids:
                return StockProductionLot.browse()
        lot = StockProductionLot.search([
            ('product_id', '=', self.product_id.id),
            ('name', '=', self.line_lot_name),
        ], limit=1)
        if not lot and create_lot:
            lot = lot.create({
                'name': self.line_lot_name,
                'product_id': self.product_id.id,
                'life_date': self.life_date,
            })
        return lot
    

