from odoo import fields, models, api


class Packaging(models.Model):
    _name="purchase.packaging"
    _rec_name="packaging"

    packaging = fields.One2many(
        comodel_name='purchase.order', inverse_name='packaging_id')
    packaging = fields.Char("Packaging")