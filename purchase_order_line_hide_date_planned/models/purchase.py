# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from datetime import datetime

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Redefine field to remove the compute function we don't need anymore.
    # Also make it required to avoid SQL constraint to show.
    # No default was set to avoid confusions to user.
    date_planned = fields.Datetime(
        string="Scheduled Date", store=True, index=True, required=False, compute=""
    )

    @api.multi
    @api.onchange("date_planned")
    def _onchange_date_planned(self):
        """Make the PO lines take in count this value as it changes"""
        for order in self:
            order.order_line.update({"date_planned": order.date_planned})


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    date_planned = fields.Datetime(string="Scheduled Date", required=False)

    @api.onchange("product_qty", "product_uom")
    def _onchange_quantity(self):
        """Inherit native method to force the PO line date_planned field to be
        the order's one."""

        for line in self:
            self.date_planned = self.order_id.date_planned
        return super(PurchaseOrderLine, self)._onchange_quantity()

    @api.model
    def _get_date_planned(self, seller, po=False):
        """Override native method to force the PO line date_planned field to be
        the order's one."""
        if self.order_id.date_planned:
            return datetime.strptime(
                self.order_id.date_planned,
                DEFAULT_SERVER_DATETIME_FORMAT
            )
        else:
            return datetime.today()
