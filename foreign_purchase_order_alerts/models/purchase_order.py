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

    is_confirmation_delayed = fields.Boolean(default=False, compute='_compute_is_confirmation_delayed', store=True)

    @api.depends('state', 'date_order', 'reception_status', 'confirmation_number', 'confirmation_date',
                 'confirmation_not_required')
    def _compute_is_confirmation_delayed(self):
        for record in self:
            if not record.confirmation_not_required:
                if not record.confirmation_number or not record.confirmation_date:
                    if record.reception_status == 'Pending':
                        date_order_to_datetime = datetime.strptime(record.date_order, "%Y-%m-%d %H:%M:%S")
                        work_days = workdays(date_order_to_datetime, datetime.today())
                        if len(work_days) > 2:
                            record.is_confirmation_delayed = True
            elif record.confirmation_not_required:
                record.is_confirmation_delayed = False

    is_proform_delayed = fields.Boolean(default=False, compute='_compute_is_proform_delayed', store=True)

    @api.depends('payment_term_id', 'date_order', 'proforma_not_required', 'proforma_number', 'proforma_date')
    def _compute_is_proform_delayed(self):
        for record in self:
            if record.payment_term_id.display_name and\
                    "anticipa" in record.payment_term_id.display_name and\
                    not record.proforma_not_required and\
                    record.reception_status == 'Pending':
                date_to_datetime = datetime.strptime(record.date_order, "%Y-%m-%d %H:%M:%S")
                work_days = workdays(date_to_datetime, datetime.today())
                if len(work_days) > 5:
                    record.is_proform_delayed = True
            elif record.reception_status != 'Pending':
                record.is_proform_delayed = False

    is_payment_TTE_delayed = fields.Boolean(default=False, compute='_compute_is_payment_TTE_delayed', store=True)

    @api.depends('date_planned', 'payment_not_required', 'payment_TTE_amount')
    def _compute_is_payment_TTE_delayed(self):
        for record in self:
            if not record.payment_not_required and \
                    record.reception_status == 'Pending':
                date_planned_to_datetime = datetime.strptime(record.date_planned, "%Y-%m-%d %H:%M:%S")
                work_days = workdays(datetime.today(), date_planned_to_datetime)
                if len(work_days) <= 5:
                    record.is_payment_TTE_delayed = True
            elif record.reception_status != 'Pending':
                record.is_payment_TTE_delayed = False

    is_booking_conveyance_empty = fields.Boolean(default=False, compute='_compute_is_booking_conveyance_empty', store=True)

    @api.depends('create_date', 'booking_not_required', 'booking_conveyance')
    def _compute_is_booking_conveyance_empty(self):
        for record in self:
            if not record.booking_not_required and \
                    record.reception_status == 'Pending':
                if not record.booking_conveyance:
                    record.is_booking_conveyance_empty = True
            elif record.reception_status != 'Pending':
                record.is_booking_conveyance_empty = False

    is_booking_ETD_date_empty = fields.Boolean(default=False, compute='_compute_is_booking_ETD_date_empty', store=True)

    @api.depends('create_date', 'booking_not_required', 'booking_ETD_date')
    def _compute_is_booking_ETD_date_empty(self):
        for record in self:
            if not record.booking_not_required and \
                    record.reception_status == 'Pending':
                if not record.booking_ETD_date:
                    record.is_booking_ETD_date_empty = True
            elif record.reception_status != 'Pending':
                record.is_booking_ETD_date_empty = False

    is_booking_ETA_date_empty = fields.Boolean(default=False, compute='_compute_is_booking_ETA_date_empty', store=True)

    @api.depends('create_date', 'booking_not_required', 'booking_ETD_date', 'booking_ETA_date')
    def _compute_is_booking_ETA_date_empty(self):
        for record in self:
            if not record.booking_not_required and \
                    record.reception_status == 'Pending':
                if record.booking_ETD_date and not record.booking_ETA_date:
                    date_ETD_to_datetime = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    work_days = workdays(datetime.today(), date_ETD_to_datetime)
                    if work_days and len(work_days) <= 15:
                        record.is_booking_ETA_date_empty = True
                    else:
                        record.is_booking_ETA_date_empty = False
                elif record.booking_ETA_date:
                    record.is_booking_ETA_date_empty = False

    is_documents_invoice_delayed = fields.Boolean(default=False, compute='_compute_is_documents_delayed', store=True)
    is_documents_shipping_delayed = fields.Boolean(default=False, compute='_compute_is_documents_delayed', store=True)
    # ME PINTA CUANDO ME FALTAN AMBOS, PERO NO CUANDO ME FALTA UNO SOLO
    @api.depends('create_date', 'documents_not_required', 'booking_not_required', 'booking_ETD_date',
                 'documents_commercial_invoice_number', 'documents_shipping_document')
    def _compute_is_documents_delayed(self):
        for record in self:
            if not record.booking_not_required and\
                    not record.documents_not_required and\
                    record.reception_status == 'Pending':
                if record.booking_ETD_date:
                    date_ETD_to_datetime = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    work_days = workdays(date_ETD_to_datetime, datetime.today())
                    if len(work_days) > 3:
                        if not record.documents_commercial_invoice_number:
                            record.is_documents_invoice_delayed = True
                        if not record.documents_shipping_document:
                            record.is_documents_shipping_delayed = True
            else:
                record.is_documents_invoice_delayed = False
                record.is_documents_shipping_delayed = False

    is_delivery_delayed = fields.Boolean(default=False, compute='_compute_is_delivery_delayed', store=True)

    @api.depends('create_date', 'delivery_not_required', 'booking_not_required', 'booking_ETD_date',
                 'delivery_number')
    def _compute_is_delivery_delayed(self):
        for record in self:
            if not record.booking_not_required and\
                    not record.delivery_not_required and\
                    record.reception_status == 'Pending' and\
                    not record.delivery_number:
                if record.booking_ETD_date:
                    date_ETD_to_datetime = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    work_days = workdays(date_ETD_to_datetime, datetime.today())
                    if len(work_days) > 3:
                        record.is_delivery_delayed = True
            else:
                record.is_delivery_delayed = False

    is_status_pending = fields.Boolean(default=False, compute='_compute_is_status_pending', store=True)

    @api.depends('create_date', 'delivery_not_required', 'booking_not_required', 'booking_ETD_date')
    def _compute_is_status_pending(self):
        for record in self:
            if record.reception_status == "Pending":
                record.is_status_pending = True
            else:
                record.is_status_pending = False
