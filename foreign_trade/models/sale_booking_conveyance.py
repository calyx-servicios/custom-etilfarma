from odoo import fields, models, _
from odoo.exceptions import Warning


class SaleBookingConveyance(models.Model):
    _name = "sale.booking.conveyance"
    _rec_name = "booking_conveyance"
    _order = "sequence"

    booking_conveyance = fields.Char("Booking Conveyance")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        sale_obj = self.env["sale.order"]
        rule_ranges = sale_obj.search([("booking_conveyance", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more sale, "
                    "try to archive it."
                )
            )
        return super(SaleBookingConveyance, self).unlink()