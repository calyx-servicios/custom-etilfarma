from odoo import fields, models, _
from odoo.exceptions import Warning


class SalePaymentInstructions(models.Model):
    _name = "sale.payment.instructions"
    _rec_name = "payment_instructions"
    _order = "sequence"

    payment_instructions = fields.Char("Payment Instructions")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        sale_obj = self.env["sale.order"]
        rule_ranges = sale_obj.search(
            [("payment_instructions_id", "=", self.id)]
        )
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more sale, "
                    "try to archive it."
                )
            )
        return super(SalePaymentInstructions, self).unlink()
