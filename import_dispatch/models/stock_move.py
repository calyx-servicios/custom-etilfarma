# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError

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
                    
    line_dispatch_name = fields.Char(
        string='Dispatch Name',
        compute=_compute_line_dispatch_name
    )

    dispatch_id = fields.Many2one(
        'stock.production.dispatch',
    )

    dispatch_name = fields.Char(
        string='Dispatch Name',
    )