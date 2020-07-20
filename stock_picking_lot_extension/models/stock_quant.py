# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    life_date = fields.Datetime(related='lot_id.life_date', store=True)
