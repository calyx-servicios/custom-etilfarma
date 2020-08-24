# Copyright 2020 Calyx S.A
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.onchange("order_type")
    def onchange_order_type_oct(self):
        if self.order_type.sequence_id.name == "Third Party Purchase Order":
            self._clean_tracking_order_fields()
            self._set_tracking_order_fields_oct()

    @api.onchange("partner_id")
    def _onchange_supplier(self):
        for record in self:
            if not self.order_type.sequence_id.name == "Third Party Purchase Order": 
                self._clean_tracking_order_fields()   
                supplier = record.partner_id
                if supplier:
                    if supplier.purchase_confirmation_not_required:
                        record.confirmation_not_required = True
                    if supplier.purchase_proforma_not_required:
                        record.proforma_not_required = True
                    if supplier.purchase_payment_not_required:
                        record.payment_not_required = True
                    if supplier.purchase_dispatcher_not_required:
                        record.dispatcher_not_required = True
                    if supplier.purchase_intervention_not_required:
                        record.intervention_not_required = True
                    if supplier.purchase_import_license_not_required:
                        record.import_license_not_required = True
                    if supplier.purchase_booking_not_required:
                        record.booking_not_required = True
                    if supplier.purchase_documents_not_required:
                        record.documents_not_required = True
                    if supplier.purchase_delivery_not_required:
                        record.delivery_not_required = True
                    if (
                        supplier.purchase_original_documentation_not_required
                    ):
                        record.original_documentation_not_required = True
                    if supplier.purchase_expenses_not_required:
                        record.expenses_not_required = True

    def _clean_tracking_order_fields(self):
        for record in self:
            record.confirmation_not_required = False
            record.proforma_not_required = False
            record.payment_not_required = False
            record.dispatcher_not_required = False
            record.intervention_not_required = False
            record.import_license_not_required = False
            record.booking_not_required = False
            record.documents_not_required = False
            record.delivery_not_required = False
            record.original_documentation_not_required = False
            record.expenses_not_required = False

    def _set_tracking_order_fields_oct(self):
        for record in self:
            record.confirmation_not_required = False
            record.proforma_not_required = False
            record.payment_not_required = False
            record.dispatcher_not_required = True
            record.intervention_not_required = True
            record.import_license_not_required = False
            record.booking_not_required = False
            record.documents_not_required = False
            record.delivery_not_required = True
            record.original_documentation_not_required = False
            record.expenses_not_required = True
