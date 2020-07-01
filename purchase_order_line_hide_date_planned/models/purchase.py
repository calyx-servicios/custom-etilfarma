# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    # Redefine field to remove the compute function we don't need anymore.
    # Also make it required to avoid SQL constraint to show.
    # No default was set to avoid confusions to user.
    date_planned = fields.Datetime(
        string="Scheduled Date", store=True, index=True, required=True, compute=""
    )

    @api.multi
    @api.onchange("date_planned")
    def onchange_date_planned(self):
        """Make the PO lines take in count this value as it changes"""
        for order in self:
            order.order_line.update({"date_planned": order.date_planned})


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    date_planned = fields.Datetime(string="Scheduled Date", required=False)

    @api.onchange("product_qty", "product_uom")
    def _onchange_quantity(self):
        """Override native method to force the PO line date_planned field to be
        the order's one. TO-DO: Do it smoothly"""
        if not self.product_id:
            return

        seller = self.product_id._select_seller(
            partner_id=self.partner_id,
            quantity=self.product_qty,
            date=self.order_id.date_order and self.order_id.date_order[:10],
            uom_id=self.product_uom,
        )

        self.date_planned = self.order_id.date_planned

        if not seller:
            return

        price_unit = (
            self.env["account.tax"]._fix_tax_included_price_company(
                seller.price,
                self.product_id.supplier_taxes_id,
                self.taxes_id,
                self.company_id,
            )
            if seller
            else 0.0
        )
        if (
            price_unit
            and seller
            and self.order_id.currency_id
            and seller.currency_id != self.order_id.currency_id
        ):
            price_unit = seller.currency_id.compute(
                price_unit, self.order_id.currency_id
            )

        if seller and self.product_uom and seller.product_uom != self.product_uom:
            price_unit = seller.product_uom._compute_price(price_unit, self.product_uom)

        self.price_unit = price_unit

    @api.model
    def _get_date_planned(self):
        """Override native method to force the PO line date_planned field to be
        the order's one."""
        return self.order_id.date_planned
