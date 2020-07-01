# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models
from odoo.addons.purchase.models.purchase import PurchaseOrder as Purchase


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    def _default_order_type(self):
        return self.env["purchase.order.type"].search([
            ("name", "=", "OCL")
        ], limit=1).id

    order_type = fields.Many2one(
        comodel_name="purchase.order.type",
        readonly=False,
        states=Purchase.READONLY_STATES,
        string="Type",
        ondelete="restrict",
        default=_default_order_type,
    )

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        When the partner changes, we get the order_type
        from the partner purchase_type field if this has
        a value
        """
        super().onchange_partner_id()
        purchase_type = (
            self.partner_id.purchase_type
            or self.partner_id.commercial_partner_id.purchase_type
        )
        if purchase_type:
            self.order_type = purchase_type

    @api.multi
    @api.onchange("order_type")
    def onchange_order_type(self):
        """
        When the order types changes, we get the incoterm from
        the order type record if this has a value.
        """
        for order in self:
            if order.order_type.incoterm_id:
                order.incoterm_id = order.order_type.incoterm_id.id

    @api.model
    def create(self, vals):
        """
        Adding the prefix number of the sequence selected
        in the purchase type.
        """
        if vals.get("name", "/") == "/" and vals.get("order_type"):
            purchase_type = self.env["purchase.order.type"].browse(
                vals["order_type"]
            )
            if purchase_type.sequence_id:
                vals["name"] = purchase_type.sequence_id.next_by_id()
        return super().create(vals)
