# Copyright 2020 Calyx Servicios S.A.
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
                 'confirmation_not_required', 'status_status')
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
        advanced_payment_term = self.env.ref('purchase_order_types.account_payment_term_advance')
        for record in self:
            if record.payment_term_id == advanced_payment_term and not record.proforma_not_required and\
                    record.reception_status == 'Pending':
                date_to_datetime = datetime.strptime(record.date_order, "%Y-%m-%d %H:%M:%S")
                work_days = workdays(date_to_datetime, datetime.today())
                if len(work_days) > 5 or not record.proforma_number or not record.proforma_date:
                    record.is_proform_delayed = True
            elif record.reception_status != 'Pending':
                record.is_proform_delayed = False

    is_payment_delayed = fields.Boolean(default=False, compute='_compute_is_payment_delayed', store=True)

    @api.depends(
        'date_order',
        'payment_term_id',
        'reception_status',
        'payment_not_required',
        'payment_TTE_amount',
        'invoice_ids',
        'invoice_ids.date_due',
        'payment_bank',
        'payment_account',
        'payment_application_number',
        'payment_date',
        'payment_reference',
        'payment_concept',
        'payment_TTE_amount',
        'payment_TC',
        'payment_currency')
    def _compute_is_payment_delayed(self):
        advanced_payment_term = self.env.ref('purchase_order_types.account_payment_term_advance')
        for record in self:
            if not record.payment_not_required and record.reception_status == 'Pending':
                if record.payment_term_id != advanced_payment_term:

                    empty_fields = False
                    if not all([record.payment_bank, record.payment_account, record.payment_application_number,
                                record.payment_date, record.payment_reference, record.payment_concept,
                                record.payment_TTE_amount, record.payment_TC, record.payment_currency]):
                        empty_fields = True

                    if record.invoice_ids:
                        for invoice in record.invoice_ids:
                            if invoice.date_due:
                                date_due = datetime.strptime(invoice.date_due, "%Y-%m-%d")
                                work_days = workdays(datetime.today(), date_due)
                                if len(work_days) <= 5 and empty_fields:
                                    record.is_payment_delayed = True

            elif record.reception_status != 'Pending':
                record.is_payment_delayed = False

    is_booking_conveyance_empty = fields.Boolean(default=False, compute='_compute_is_booking_conveyance_empty', store=True)


    @api.depends('date_order', 'booking_not_required', 'booking_conveyance_id')
    def _compute_is_booking_conveyance_empty(self):
        for record in self:
            if not record.booking_not_required and \
                    record.reception_status == 'Pending':
                if not record.booking_conveyance_id:
                    record.is_booking_conveyance_empty = True
            elif record.reception_status != 'Pending':
                record.is_booking_conveyance_empty = False

    is_booking_ship_name_empty = fields.Boolean(default=False, compute='_compute_is_booking_ship_name_empty', store=True)
    
    @api.depends('date_order', 'booking_not_required', 'booking_ship_name')
    def _compute_is_booking_ship_name_empty(self):
        for record in self:
            if not record.booking_not_required and \
                    record.reception_status == 'Pending':
                if not record.booking_ship_name:
                    record.is_booking_ship_name_empty = True
            elif record.reception_status != 'Pending':
                record.is_booking_ship_name_empty = False

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
                    date_ETD = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    delta_days = datetime.today() - date_ETD
                    if delta_days and delta_days.days <= 15:
                        record.is_booking_ETA_date_empty = True
                    else:
                        record.is_booking_ETA_date_empty = False
                elif record.booking_ETA_date:
                    record.is_booking_ETA_date_empty = False

    is_documents_invoice_delayed = fields.Boolean(default=False, compute='_compute_is_documents_delayed', store=True)
    is_documents_shipping_delayed = fields.Boolean(default=False, compute='_compute_is_documents_delayed', store=True)

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

    @api.depends('date_order', 'delivery_not_required', 'booking_not_required', 'booking_ETD_date',
                 'delivery_number', 'delivery_official_date', 'delivery_chanel_id')
    def _compute_is_delivery_delayed(self):
        for record in self:
            if not record.booking_not_required and\
                    not record.delivery_not_required and\
                    record.reception_status == 'Pending':
                if record.booking_ETD_date:
                    date_ETD_to_datetime = datetime.strptime(record.booking_ETD_date, "%Y-%m-%d")
                    work_days = workdays(date_ETD_to_datetime, datetime.today())
                    if len(work_days) > 3:
                        record.is_delivery_delayed = True
                    elif not all([record.delivery_number, record.delivery_official_date, record.delivery_chanel_id]):
                        record.is_delivery_delayed = True
                    else:
                        record.is_delivery_delayed = False
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

    is_import_license_official_date_pending = fields.Boolean(
        default=False,
        compute="_compute_is_license_official_date_pending",
        store=True,
    )

    @api.depends(
        "proforma_date",
        "import_license_not_required",
        "import_license_official_date",
        "proforma_not_required",
    )
    def _compute_is_license_official_date_pending(self):
        for record in self:
            if (
                record.proforma_not_required
                and not record.import_license_official_date
            ):
                record.is_import_license_official_date_pending = True
                
            elif (
                record.proforma_date
                and not record.import_license_official_date
            ):
                record.is_import_license_official_date_pending = True
            else:
                record.is_import_license_official_date_pending = False
            
            if record.import_license_not_required:
                record.is_import_license_official_date_pending = False

    is_original_documentation_delayed = fields.Boolean(
        default=False,
        compute='_is_original_documentation_delayed',
        tore=True
    )

    @api.depends(
        "original_documentation_not_required",
        "booking_ETA_date",
        "original_documentation_original_receipt_date",
    )
    def _is_original_documentation_delayed(self):
        for record in self:
            if (
                not record.original_documentation_not_required
                and record.booking_ETA_date
            ):
                if (
                    not record.original_documentation_original_receipt_date
                ):
                    date_ETA_to_datetime = datetime.strptime(
                        record.booking_ETA_date, "%Y-%m-%d"
                    )
                    work_days = workdays(
                        date_ETA_to_datetime, datetime.today()
                    )
                    if len(work_days) > 10:
                        record.is_original_documentation_delayed = True
            else:
                record.is_original_documentation_delayed = False
