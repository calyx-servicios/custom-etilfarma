from odoo import fields, models, api, _


class ProductTemplate(models.Model):
    _inherit = "product.template"

    intervention_types = fields.Many2many(
        comodel_name="purchase.order.interventions", string="Intervention Types")