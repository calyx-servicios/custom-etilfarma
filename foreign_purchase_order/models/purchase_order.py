# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_type_name = fields.Char(
        string="Order Type Name", related="order_type.name"
    )
