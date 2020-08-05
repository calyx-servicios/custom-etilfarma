# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def check_confirmation_fields_ok(self):
        if not self.order_type.foreign_order:
            return True
        else:
            if (
                not self.confirmation_number
                or not self.confirmation_date
            ):
                return False
            else:
                return True
