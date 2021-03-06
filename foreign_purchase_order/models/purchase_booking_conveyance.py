from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseBookingConveyance(models.Model):
    _name = "purchase.booking.conveyance"
    _rec_name = "booking_conveyance"
    _order = "sequence"

    booking_conveyance = fields.Char("Booking Conveyance")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("booking_conveyance", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseBookingConveyance, self).unlink()