# Copyright 2020 Calyx S.A
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ExceptionRule(models.Model):
    _inherit = "exception.rule"

    block_oct = fields.Boolean("Block OCT")
