# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta

from odoo import fields, models, api, _


def workdays(d, end, excluded=(6, 7)):
    days = []
    while d.date() <= end.date():
        if d.isoweekday() not in excluded:
            days.append(d)
        d += timedelta(days=1)
    return days


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    is_three_days_since_ETD = fields.Boolean(default=False, compute='_compute_is_three_days_since_ETD', store=True)

    @api.depends('booking_not_required', 'booking_ETD_date')
    def _compute_is_three_days_since_ETD(self):
        for record in self:
            if not record.booking_not_required:
                if record.booking_ETD_date:
                    ETD_date = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    work_days = workdays(ETD_date, datetime.today())
                    if len(work_days) > 3:
                        record.is_three_days_since_ETD = True
