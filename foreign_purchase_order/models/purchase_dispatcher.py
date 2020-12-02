from odoo import fields, models, api, _
from odoo.exceptions import Warning, UserError
import re


class PurchaseDispatcher(models.Model):
    _name = "purchase.dispatcher"
    _rec_name = "name"
    _order = "sequence"

    name = fields.Char(string="Name")
    address = fields.Char(string="Address")
    email = fields.Char(string="Email")
    phone_number = fields.Char(string="Phone Number")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    @api.constrains('phone_number')
    def _check_format_phone_number(self):
        for rec in self:
            if rec.phone_number:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.phone_number)
                if match == None:
                    raise UserError("phone number invalid format")

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("dispatcher", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseDispatcher, self).unlink()