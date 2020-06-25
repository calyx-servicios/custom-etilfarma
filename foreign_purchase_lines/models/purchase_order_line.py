# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api
import logging

_logger = logging.getLogger(__name__)


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    @api.depends("product_id")
    def _available_packaging_leads_ids(self):
        for record in self:
            product_id = record.product_id
            packaging_obj = self.env["purchase.product.packaging"]
            domain = [
                (
                    "packaging_lines.product_id",
                    "=",
                    product_id.product_tmpl_id.id,
                )
            ]
            packaging_ids = packaging_obj.search(domain)

            record.available_packaging_ids = packaging_ids

    packaging = fields.Many2many(
        comodel_name="purchase.product.packaging", string="Packaging"
    )

    available_packaging_ids = fields.Many2many(
        comodel_name="purchase.product.packaging",
        string="Packaging",
        compute="_available_packaging_leads_ids",
    )

    product_nmc = fields.Char(string="NMC", related="product_id.product_nmc")
    country_id = fields.Many2one(comodel_name="res.country", string="Origin")
    observactions = fields.Char(string="Observation")
