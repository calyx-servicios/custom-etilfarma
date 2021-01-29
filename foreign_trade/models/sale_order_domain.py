from odoo import fields, models, api

class SaleOrderDomain(models.AbstractModel):
    _inherit = "sale.order"
    
    """
        Below are all the conditions for an order to be incomplete
    """
    def _get_domain_sale_international(self):
        return [
            '&', ('order_type_foreign', '=', True),
            ('state', 'in', ['sale', 'draft', 'sent']),
        ]

    def _get_domain_incomplete_confirmation(self):
        return [
            '&', '&',('confirmation_not_required', '=', False), ('sale_international', '=', True),
            '|' , ('confirmation_number', '=', False), ('confirmation_date' , '=' , False)
        ]

    def _get_domain_incomplete_proform(self):
        return [
            '&', '&',('proforma_not_required', '=', False), ('sale_international', '=', True),
            ('proforma_number', '=', False),
        ]

    def _get_domain_incomplete_invoice(self):
        return [
            '&', '&',('invoice_not_required', '=', False), ('sale_international', '=', True),
            ('invoice_number', '=', False),
        ]

    def _get_domain_incomplete_payment(self):
        return [
            '&', '&',('payment_not_required', '=', False), ('sale_international', '=', True),
            '|', '|', '|',
            ('payment_bank', '=', False),
            ('payment_date', '=', False),
            ('payment_concept', '=', False),
            ('payment_tre', '=', False)
        ]

    def _get_domain_incomplete_dispatcher(self):
        return [
            '&', '&',('dispatcher_not_required', '=', False), ('sale_international', '=', True),
            ('dispatcher_reference', '=', False)
        ]

    def _get_domain_incomplete_license(self):
        return [
            '&', '&',('shipping_license_not_required', '=', False), ('sale_international', '=', True),
            '|', '|',
            ('shipping_license_channel', '=', False),
            ('shipping_license_number', '=', False),
            ('shipping_license_official_date', '=', False),
            ('estimated_shipping_date', '=', False),
        ]

    def _get_domain_incomplete_booking(self):
        return [
            '&', '&',('booking_not_required', '=', False), ('sale_international', '=', True),
            '|', '|', '|',
            ('booking_conveyance_id', '=', False),
            ('booking_ETD_date', '=', False),
            ('booking_ETA_date', '=', False),
            ('booking_transport_company', '=', False),
        ]

    def _get_domain_incomplete_documents(self):
        return [
            '&', '&',('transport_doc_not_required', '=', False), ('sale_international', '=', True),
            '|', ('transport_doc_documents', '=', False), ('transport_doc_date', '=', False),
        ]

    def _get_domain_incomplete_certificate_of_analysis(self):
        return [
            '&', '&',('certificate_of_analysis_not_required' , '=' , False), ('sale_international', '=', True),
            ('certificate_of_analysis_shipment_date_to_customer', '=', False),
        ]

    def _get_domain_incomplete_origin(self):
        return [
            '&', '&',('origin_not_required', '=', False), ('sale_international', '=', True),
            '|',
            ('origin_reference', '=', False),
            ('origin_shipment_date', '=', False),
        ]

    def _get_domain_incomplete_expenses(self):
        return [
            '&', '&',('expenses_not_required', '=', False), ('sale_international', '=', True),
            '|', ('expenses_dispatcher_fees', '=', False), ('expenses_expenses', '=', False),
        ]

    def _get_domain_incomplete_quotation(self):
        return [
            '&', '&',('quotation_not_required', '=', False), ('sale_international', '=', True),
            '|', '|',
            ('quotation_number', '=', False),
            ('quotation_date', '=', False),
            ('quotation_client', '=', False),
        ]