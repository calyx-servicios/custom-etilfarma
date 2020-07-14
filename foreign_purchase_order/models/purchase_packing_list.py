from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchasePackingList(models.Model):
    _name = "purchase.packing.list"
    _rec_name = "packing_list"
    _order = "sequence"

    packing_list = fields.Char("Packing List")
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("packing_list_id", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchasePackingList, self).unlink()
