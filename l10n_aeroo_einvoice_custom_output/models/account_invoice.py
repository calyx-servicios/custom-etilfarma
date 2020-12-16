# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_sale_id(self):
        sale_obj = self.env["sale.order"]
        sale_id = sale_obj.search(
            [("invoice_ids", "in", self.ids)], limit=1
        )
        if sale_id:
            self.sale_order_id = sale_id.id

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale order", compute="_get_sale_id"
    )
