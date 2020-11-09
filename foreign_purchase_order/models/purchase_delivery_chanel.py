from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseDeliveryChanel(models.Model):
    _name = "purchase.delivery.chanel"
    _rec_name = "delivery_chanel"
    _order = "sequence"

    delivery_chanel = fields.Char("Delivery Chanel")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("delivery_chanel", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseDeliveryChanel, self).unlink()