from odoo import fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    date_picker = fields.Date(
        string="Date Picker",
        related="purchase_id.delivery_date_planned_date",
    )
