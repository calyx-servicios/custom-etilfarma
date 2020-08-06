# Copyright 2020 Calyx S.A
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class PurchaseExceptionConfirm(models.TransientModel):

    _inherit = "purchase.exception.confirm"

    @api.multi
    def action_confirm(self):
        if self.ignore and self._context.get("oct_exceptions", False):
            self.related_model_id.ignore_exception_oct = True
            self.ignore = False
        return super(PurchaseExceptionConfirm, self).action_confirm()
