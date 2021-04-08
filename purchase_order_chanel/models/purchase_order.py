# Copyright 2021 Calyx Servicios S.A
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import models, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    chanel_id = fields.Many2one(
        "purchase.order.chanel", string="Chanel"
    ) 