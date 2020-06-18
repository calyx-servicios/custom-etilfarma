# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_type_name = fields.Char(
        string="Order Type Name",
        # related="order_type.name"
    )

    customer_purchase_order = fields.Char(string="Customer Purchase Order")
    place_of_delivery_id = fields.Many2one(
        comodel_name='purchase.delivery' ,string="Place of Delivery")
    packaging_id = fields.Many2one(
        comodel_name='purchase.packaging' ,string="Packaging")
    delivery_date_week = fields.Char(string='Delivery Date (Week)', compute='_compute_delivery_date_week', store=True)
    

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """
        When the order types changes, we search the order type OCE id
        and compares with the order type seleted by the user
        if is the same then set the order_type_name to 'OCE'
        this is for show some fields in the purchase form view
        if not then clean the values of customer_purchase_order and
        order_type_name.
        """
        oce = self.env.ref("purchase_order_types.po_type_blanket")
        for record in self:
            if record.order_type:
                if record.order_type.id == oce.id:
                    record.order_type_name = "OCE"
                else:
                    record.customer_purchase_order = ""
                    record.order_type_name = ""
            else:
                record.customer_purchase_order = ""
                record.order_type_name = ""

    @api.depends('date_planned')
    def _compute_delivery_date_week(self):
        """
        We take the date_planned assigned by the user to
        format it into the regular format.
        Then we concatenate a string with that formmated
        date plus the week number
        """
        for po in self:
            if po.date_planned:
                date_fmt = '/'.join(reversed(po.date_planned.split(' ')[0].split('-')))
                po.delivery_date_week = '{} - W{}'.format(
                    date_fmt,
                    datetime.strptime(po.date_planned, '%Y-%m-%d %H:%M:%S').isocalendar()[1]
                )
