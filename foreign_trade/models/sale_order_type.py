from odoo import api, fields, models


class SaleOrderType(models.Model):
    _name = "sale.order.type"
    _description = "Type of sale order"
    _order = "sequence"

    @api.model
    def _default_sequence_id(self):
        seq_type = self.env.ref("sale.seq_sale_order")
        return seq_type.id

    name = fields.Char(required=True)
    active = fields.Boolean(default=True)
    description = fields.Text(string="Description", translate=True)
    sequence_id = fields.Many2one(
        comodel_name="ir.sequence",
        string="Entry Sequence",
        copy=False,
        domain=[("sale_seq", "=", "True")],
        default=_default_sequence_id,
        required=True,
    )

    incoterm_id = fields.Many2one(
        comodel_name="stock.incoterms", string="Incoterm"
    )
    sequence = fields.Integer(default=10)
    foreign_order = fields.Boolean(string="Foreign Order?")
