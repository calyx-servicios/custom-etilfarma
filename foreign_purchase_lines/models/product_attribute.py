# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class ProductAttribute(models.Model):
    _inherit = "product.attribute"

    packaging = fields.Boolean(string="Packaging", default=False)

    @api.onchange("packaging")
    def _onchange_packaging(self):
        """ 
            Validate that only one attribute have the 
            packaging option as a True
        """
        for record in self:
            if record.packaging:
                product_attribute_obj = self.env["product.attribute"]
                domain = [("packaging", "=", True)]
                attribute_ids = product_attribute_obj.search(domain)
                if attribute_ids:
                    self.env.user.notify_warning(
                        "Only one attribute can have packaging option.",
                        "Warning",
                        1,
                    )
                    record.packaging = False

    @api.multi
    def unlink(self):
        """
            Add verification to the unlink function, we can't delete
            a record if this have a packaging option as true.
        """
        for record in self:
            if record.packaging:
                raise UserError(
                    _(
                        "You cannot delete a attribute with packaging option, "
                        "please contact an admin."
                    )
                )
        return super(ProductAttribute, self).unlink()
