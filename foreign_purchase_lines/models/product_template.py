# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.template"

    def _get_default_code(self):
        res = self.env['ir.sequence'].next_by_code('product.default.code')
        return res

    default_code = fields.Char('Internal Reference', index=True,
                               default=_get_default_code)
                               
    product_nmc = fields.Char(string="HS Code")
    hs_code = fields.Char(string="HS Code", help="Standardized code for international shipping and goods declaration")
    maker_id = fields.Char(string="Maker")
    order_date = fields.Date(string="Order date")
    country_id = fields.Many2one(comodel_name="res.country", string="Origin")

    @api.model
    def create(self, vals):
        """
            Limit the number of attributes.
        """
        lines = vals.get("attribute_line_ids")
        if lines:
            lines = len(lines)
            if lines > 1:
                raise UserError(_("Limit to only 1 variant"))
        return super().create(vals)

    @api.multi
    def write(self, vals):
        """
            Limit the number of attributes.
        """
        lines = vals.get("attribute_line_ids")
        if lines:
            lines = len(lines)
            if lines > 1:
                raise UserError(_("Limit to only 1 variant"))
        return super().write(vals)
