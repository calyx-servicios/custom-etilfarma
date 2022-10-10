# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api
from . import conversor


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def _get_sale_id(self):
        sale_obj = self.env["sale.order"]
        sale_id = sale_obj.search(
            [("name", "=", self.origin)], limit=1
        )
        if sale_id:
            self.sale_order_id = sale_id.id
        else:
            self.sale_order_id = False

    sale_order_id = fields.Many2one(
        "sale.order", string="Sale order", compute="_get_sale_id"
    )

    @api.multi
    def invoice_en_print(self):
        """
        Print the Einvoice custom report and mark it as sent.
        """
        self.sent = True
        return self.env.ref(
            "l10n_aeroo_einvoice_custom_output.action_aeroo_report_ar_einvoice_en"
        ).report_action(self)

    @api.multi
    def number2word_en(self, number):
        num = str(number)
        word = conversor.dollars2words(num)
        return word.capitalize()
