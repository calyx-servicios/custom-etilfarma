from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def check_date(self, rec, date, field):
        if rec.create_date and date:
            if rec.create_date[:10] > date[:10]:
                raise ValidationError(_('%s must not be prior to the Creation Date') %
                                      rec._fields[field]._description_string(rec.env))
        elif date:
            if datetime.strftime(datetime.now(), '%Y-%m-%d') > date[:10]:
                raise ValidationError(_('%s must not be prior to the Creation Date') %
                                      rec._fields[field]._description_string(rec.env))

    @api.constrains(
        'date_planned',
        'delivery_official_date',
        'confirmation_date',
        'proforma_date',
        'payment_date',
        'intervention_application_date',
        'intervention_approval_date',
        'import_license_official_date',
        'import_license_approval_date',
        'booking_ETD_date',
        'booking_ETA_date',
        'documents_FC_date',
        'documents_quality_certificate_approval_date',
        'documents_shipping_date',
        'documents_date_shipment_originals',
        'delivery_official_date',
        'original_documentation_original_receipt_date'
    )
    def constraint_dates_to_restrict(self):
        fields_check = ('date_planned',
                        'delivery_official_date',
                        'confirmation_date',
                        'proforma_date',
                        'payment_date',
                        'intervention_application_date',
                        'intervention_approval_date',
                        'import_license_official_date',
                        'import_license_approval_date',
                        'booking_ETD_date',
                        'booking_ETA_date',
                        'documents_FC_date',
                        'documents_quality_certificate_approval_date',
                        'documents_shipping_date',
                        'documents_date_shipment_originals',
                        'delivery_official_date',
                        'original_documentation_original_receipt_date')
        for rec in self:
            for field in fields_check:
                self.check_date(rec, getattr(rec, field), field)
