# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_type_name = fields.Char(
        string="Order Type Name",
        # related="order_type.name"
    )

    order_type_blanket = fields.Boolean(string="Blanket", default=False)

    purchase_sample = fields.Boolean(string="Sample?")

    customer_purchase_order = fields.Char(string="Customer Purchase Order")
    place_of_delivery_id = fields.Many2one(
        comodel_name="purchase.delivery", string="Place of Delivery"
    )
    packaging_id = fields.Many2one(
        comodel_name="purchase.packaging", string="Packaging"
    )

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """
        When the order type changes, check if that order is a blanket order
        if it is, then set like True the variable order_type_blanket to show some fields in
        the purchase view.
        """
        # oce = self.env.ref("purchase_order_types.po_type_blanket")
        for record in self:
            if record.order_type:
                # if record.order_type.id == oce.id:
                # record.order_type_name = "OCE"
                if record.order_type.blanket:
                    record.order_type_blanket = True
                else:
                    record.customer_purchase_order = ""
                    record.order_type_blanket = False

                    # record.order_type_name = ""
            else:
                record.customer_purchase_order = ""
                record.order_type_blanket = False

                # record.order_type_name = ""

    @api.onchange("purchase_sample")
    def _onchange_purchase_sample(self):
        """
         Set the order type in OCM
        """
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        for record in self:
            if ocm:
                record.order_type = ocm.id
                if ocm.blanket:
                    record.order_type_blanket = True
                # record.order_type_name = "OCM"
