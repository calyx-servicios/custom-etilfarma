from odoo import fields, models, _
from odoo.exceptions import Warning


class SaleShipment(models.Model):
    _name = "sale.shipment"
    _rec_name = "shipment"
    _order = "sequence"

    shipment = fields.Char("Shipment")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        sale_obj = self.env["sale.order"]
        rule_ranges = sale_obj.search([("shipment_id", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more sale, "
                    "try to archive it."
                )
            )
        return super(SaleShipment, self).unlink()
