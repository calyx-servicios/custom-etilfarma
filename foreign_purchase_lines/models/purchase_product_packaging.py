# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class PurchaseProductPackaging(models.Model):
    _name = "purchase.product.packaging"
    _description = "Type of product's packaging"

    def _default_order_type(self):
        return self.env["purchase.packaging.type"].search([], limit=1)

    name = fields.Char(string="Name", default="New")
    packaging_type_id = fields.Many2one(
        comodel_name="purchase.packaging.type",
        ondelete="restrict",
        string="Type",
        default=_default_order_type,
        required=True,
    )
    qty = fields.Integer(string="Qty.", required=True)
    packaging_lines = fields.One2many(
        comodel_name="purchase.product.packaging.line",
        inverse_name="packaging_id",
        string="Products",
    )
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    @api.model
    def create(self, vals):
        """
        Name is create based in the type of packaging and the qty.
        """
        packaging_type_id = vals.get("packaging_type_id")
        qty = vals.get("qty")
        packaging_type = self.env["purchase.packaging.type"].browse(
            packaging_type_id
        )
        if packaging_type and qty:
            vals["name"] = str(packaging_type.name) + " - " + str(qty)
        return super().create(vals)

    @api.multi
    def write(self, vals):
        """
        Name is edit based in the type of packaging and the qty.
        """
        packaging_type = vals.get("packaging_type_id")
        qty = vals.get("qty")

        if not packaging_type:
            packaging_type = self.packaging_type_id
        if not qty:
            qty = self.qty

        if packaging_type and qty:
            vals["name"] = str(packaging_type.name) + " - " + str(qty)
        return super().write(vals)


class PurchaseProductPackagingLines(models.Model):
    _name = "purchase.product.packaging.line"
    _description = "Products in packaging"

    name = fields.Char(string="Name")
    packaging_id = fields.Many2one(
        comodel_name="purchase.product.packaging", string="Packaging"
    )
    product_id = fields.Many2one(
        comodel_name="product.template", string="Product"
    )
