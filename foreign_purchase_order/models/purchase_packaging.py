from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchasePackaging(models.Model):
    _name = "purchase.packaging"
    _rec_name = "packaging"
    _order = "sequence"

    packaging = fields.Char("Packaging")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("packaging_id", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchasePackaging, self).unlink()
