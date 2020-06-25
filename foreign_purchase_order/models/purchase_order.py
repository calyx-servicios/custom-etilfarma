# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # order_type_name = fields.Char(
    #     string="Order Type Name",
    #     # related="order_type.name"
    # )

    order_type_blanket = fields.Boolean(string="Blanket", default=False)

    purchase_sample = fields.Boolean(string="Sample?", default=False)

    customer_purchase_order = fields.Char(string="Customer Purchase Order")
    place_of_delivery_id = fields.Many2one(
        comodel_name="purchase.delivery", string="Place of Delivery"
    )
    packaging_id = fields.Many2one(
        comodel_name="purchase.packaging", string="Packaging"
    ) 
    delivery_date_week = fields.Char(
        string="Delivery Date (Week)",
        compute="_compute_delivery_date_week",
        store=True,
    )

    extra_notes = fields.Text(string="Extra", size=150)

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """
        When the order type changes, check if that order is a blanket order
        if it is, then set like True the variable order_type_blanket to show
        some fields in
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

    @api.depends("date_planned")
    def _compute_delivery_date_week(self):
        """
        We take the date_planned assigned by the user to
        format it into the regular format.
        Then we concatenate a string with that formmated
        date plus the week number
        """
        for po in self:
            if po.date_planned:
                date_fmt = "/".join(
                    reversed(po.date_planned.split(" ")[0].split("-"))
                )
                po.delivery_date_week = "{} - W{}".format(
                    date_fmt,
                    datetime.strptime(
                        po.date_planned, "%Y-%m-%d %H:%M:%S"
                    ).isocalendar()[1],
                )
                # record.order_type_name = ""

    @api.onchange("purchase_sample")
    def _onchange_purchase_sample(self):
        """
         Set the order type in OCM
        """
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        ocl = self.env.ref("purchase_order_types.po_type_regular")
        for record in self:
            if ocm:
                if record.purchase_sample:
                    record.order_type = ocm.id
                    if ocm.blanket:
                        record.order_type_blanket = True
                else:
                    if ocl:
                        record.order_type = ocl.id

