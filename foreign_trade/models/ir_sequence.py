# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'ir.sequence'

    sale_seq = fields.Boolean(
        string='Sale Order Sequence')
