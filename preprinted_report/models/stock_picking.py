from odoo import api, fields, models, _
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def pre_print(self):
        """
        Print the Einvoice custom report and mark it as sent.
        """
        self.sent = True
        return self.env.ref(
            "prueba_preprinted.pre_printed"
        ).report_action(self)
