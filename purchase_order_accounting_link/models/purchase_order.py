# Copyright 2020 Calyx S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    purchase_order_accounting = fields.Boolean(
        string="Is created from Accounting App"
    )

    @api.model
    def default_get(self, fields):
        res = super(PurchaseOrder, self).default_get(fields)
        res.update({
            'purchase_order_accounting': self._context.get('purchase_order_accounting', False)
        })
        return res
