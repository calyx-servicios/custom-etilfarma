# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class PurchaseProductPackaging(models.Model):
    _name = "purchase.packaging.type"
    _description = "Type of packaging"

    name = fields.Char(string="Name")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
