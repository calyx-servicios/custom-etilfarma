# Copyright 2020 Calyx S.A
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, fields


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    ignore_exception_oct = fields.Boolean(
        "Ignore Exceptions OCT", copy=False,
    )

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

    @api.multi
    def button_confirm_third_party(self):
        if self.detect_oct_exceptions():
            return self.with_context(
                oct_exceptions=True
            )._popup_exceptions()
        else:
            return super(
                PurchaseOrder, self
            ).button_confirm_third_party()

    @api.multi
    def detect_oct_exceptions(self):
        """returns the list of exception_ids for all the considered purchase 
        orders as a side effect, the purchase order's exception_ids column is
        updated with the list of exceptions related to the SO
        """
        exception_obj = self.env["exception.rule"]
        order_exceptions = exception_obj.search(
            [("model", "=", "purchase.order"), ("block_oct", "=", True)]
        )
        line_exceptions = exception_obj.search(
            [
                ("model", "=", "purchase.order.line"),
                ("block_oct", "=", True),
            ]
        )

        all_exception_ids = []
        for order in self:
            if order.ignore_exception or order.ignore_exception_oct:
                continue
            exception_ids = order._detect_exceptions(
                order_exceptions, line_exceptions
            )
            order.exception_ids = [(6, 0, exception_ids)]
            all_exception_ids += exception_ids
        return all_exception_ids

    # Improvement to be able to send things by context to the
    # pop up of exceptions
    @api.multi
    def _popup_exceptions(self):
        action = super(PurchaseOrder, self)._popup_exceptions()
        ctx = self._context.copy()
        ctx.update(
            {
                "active_id": self.ids[0],
                "active_ids": self.ids,
                "active_model": self._name,
            }
        )
        action.update({"context": ctx})
        return action
