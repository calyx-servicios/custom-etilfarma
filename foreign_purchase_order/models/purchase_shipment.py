from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseShipment(models.Model):
    _name = "purchase.shipment"
    _rec_name = "shipment"
    _order = "sequence"

    shipment = fields.Char("Shipment")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("shipment_id", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseShipment, self).unlink()
