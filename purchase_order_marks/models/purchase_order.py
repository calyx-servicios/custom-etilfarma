# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    marks = fields.Char(string="Marks")

    @api.onchange("order_type")
    def onchange_order_type_marks(self):
        for record in self:
            if (
                record.order_type.id
                == self.env.ref(
                    "purchase_order_invoice_to.po_type_third_party"
                ).id
            ):
                record.marks = ""
            else:
                if record.order_type_foreign:
                    if record.env.user.company_id:
                        record.marks = record.env.user.company_id.marks or ""

    @api.onchange("invoice_to")
    def onchange_order_type_invoice_to(self):
        for record in self:
            if record.invoice_to.marks:
                record.marks = record.invoice_to.marks
            else:
                record.marks = ""
