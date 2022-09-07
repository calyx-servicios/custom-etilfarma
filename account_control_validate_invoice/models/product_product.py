from odoo import fields, models

class Product(models.Model):
    _inherit = "product.product"

    gross_weight = fields.Float(digits=(12,2))
    quantity_per_package = fields.Float(digits=(12,2))