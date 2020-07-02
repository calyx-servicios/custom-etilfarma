# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api
import locale
import dateutil.parser


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def print_purchase_foreign_report(self):
        return self.env.ref(
            "purchase_order_foreign_report.action_report_purchase_foreign"
        ).report_action(self)

    def get_date_format_english(self):
        """
            Get the date of the order 
            and return in english format
        """
        for order in self:
            locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
            date = order.date_order
            city = str(order.company_id.state_id.name)
            date = dateutil.parser.parse(date).date()
            new_date = date.strftime("%A, %B %dth, %Y")
            new_format_date = city + ", " + new_date
            return new_format_date
