# Copyright 2020 Calyx Servicios S.A
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseOrderChanel(models.Model):
    _name = "purchase.order.chanel"
    _rec_name = "name"
    _order = "sequence"

    name = fields.Char(string="Chanel")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_order = self.env["purchase.order"]
        rule_ranges = purchase_order.search([("name", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseOrderChanel, self).unlink()