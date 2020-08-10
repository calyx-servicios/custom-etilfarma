# Copyright 2020 Calyx S.A
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, fields, api


class ResParnter(models.Model):
    _inherit = "res.partner"

    purchase_confirmation_not_required = fields.Boolean(
        string="Confirmation Not Required"
    )
    purchase_proforma_not_required = fields.Boolean(
        string="Proforma Not Required"
    )
    purchase_payment_not_required = fields.Boolean(
        string="Payment Not Required"
    )
    purchase_dispatcher_not_required = fields.Boolean(
        string="Dispatcher Not Required"
    )
    purchase_intervention_not_required = fields.Boolean(
        string="Intervention Not Required"
    )
    purchase_import_license_not_required = fields.Boolean(
        string="Import License Not Required"
    )
    purchase_booking_not_required = fields.Boolean(
        string="Booking Not Required"
    )
    purchase_documents_not_required = fields.Boolean(
        string="Documents Not Required"
    )
    purchase_delivery_not_required = fields.Boolean(
        string="Delivery Not Required"
    )
    purchase_original_documentation_not_required = fields.Boolean(
        string="Original Documentaion Not Required"
    )
    purchase_expenses_not_required = fields.Boolean(
        string="Expenses Not Required"
    )

    @api.onchange("supplier")
    def _onchange_supplier_purchase_fields(self):
        for record in self:
            if not record.supplier:
                self._clean_purchase_not_required_fields()

    def _clean_purchase_not_required_fields(self):
        for record in self:
            record.purchase_confirmation_not_required = False
            record.purchase_proforma_not_required = False
            record.purchase_payment_not_required = False
            record.purchase_dispatcher_not_required = False
            record.purchase_intervention_not_required = False
            record.purchase_import_license_not_required = False
            record.purchase_booking_not_required = False
            record.purchase_documents_not_required = False
            record.purchase_delivery_not_required = False
            record.purchase_original_documentation_not_required = False
            record.purchase_expenses_not_required = False
