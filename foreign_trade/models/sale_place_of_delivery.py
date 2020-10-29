from odoo import fields, models, _
from odoo.exceptions import Warning


class SalePlaceOfDeliver(models.Model):
    _name = "sale.delivery"
    _rec_name = "place_of_delivery"
    _order = "sequence"

    place_of_delivery = fields.Char("Place of Delivery")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        sale_obj = self.env["sale.order"]
        rule_ranges = sale_obj.search(
            [("place_of_delivery_id", "=", self.id)]
        )
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more sale, "
                    "try to archive it."
                )
            )
        return super(SalePlaceOfDeliver, self).unlink()
