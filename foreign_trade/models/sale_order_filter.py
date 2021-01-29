from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = "sale.order"

    incomplete_traking_order_data = fields.Boolean(
        string = "Incomplete tracking order data",
        compute = "compute_incomplete_traking_order_data",
        store = True,
    )

    incomplete_confirmation = fields.Boolean(
        string = "Incomplete Confirmation",
        compute = "compute_incomplete_confirmation",
        store = True,
    )

    sale_international = fields.Boolean(
        string = "Is sale International",
        compute = "compute_sale_international",
        store = True,
    )

    incomplete_proform = fields.Boolean(
        string = "Incomplete Proform",
        compute = "compute_incomplete_proform",
        store = True,
    )

    incomplete_invoice = fields.Boolean(
        string = "Incomplete Invoice",
        compute = "compute_incomplete_invoice",
        store = True,
    )

    incomplete_payment = fields.Boolean(
        string = "Incomplete Payment",
        compute = "compute_incomplete_payment",
        store = True,
    )

    incomplete_dispatcher = fields.Boolean(
        string = "Incomplete Dispatcher",
        compute = "compute_incomplete_dispatcher",
        store = True,
    )

    incomplete_license = fields.Boolean(
        string = "Incomplete License",
        compute = "compute_incomplete_license",
        store = True,
    )

    incomplete_booking = fields.Boolean(
        string = "Incomplete Booking",
        compute = "compute_incomplete_booking",
        store = True,
    )

    incomplete_documents = fields.Boolean(
        string = "Incomplete Documents",
        compute = "compute_incomplete_documents",
        store = True,
    )

    incomplete_certificate_of_analysis = fields.Boolean(
        string = "Incomplete Certificate of Analysis",
        compute = "compute_incomplete_certificate_of_analysis",
        store = True,
    )

    incomplete_origin = fields.Boolean(
        string = "Incomplete Origin",
        compute = "compute_incomplete_origin",
        store = True,
    )

    incomplete_expenses = fields.Boolean(
        string = "Incomplete Expenses",
        compute = "compute_incomplete_expenses",
        store = True,
    )

    incomplete_quotation = fields.Boolean(
        string = "Incomplete Quotation",
        compute = "compute_incomplete_quotation",
        store = True,
    )

    @api.multi
    @api.depends("order_type_foreign","state")
    def compute_sale_international(self):
        domain_sale_international = self.search(self._get_domain_sale_international())
        for rec in self:
            if rec in domain_sale_international:
                rec.sale_international = True
            else:
                rec.sale_international = False

    @api.multi
    @api.depends("confirmation_not_required","confirmation_number","confirmation_date","sale_international")
    def compute_incomplete_confirmation(self):
        domain_incomplete_confirmation = self.search(self._get_domain_incomplete_confirmation())
        for rec in self:
            if rec in domain_incomplete_confirmation:
                rec.incomplete_confirmation = True
            else:
                rec.incomplete_confirmation = False

    @api.multi
    @api.depends("proforma_not_required","proforma_number","sale_international")
    def compute_incomplete_proform(self):
        domain_incomplete_proform = self.search(self._get_domain_incomplete_proform())
        for rec in self:
            if rec in domain_incomplete_proform:
                rec.incomplete_proform = True
            else:
                rec.incomplete_proform = False
    
    @api.multi
    @api.depends("invoice_not_required","invoice_number","sale_international")
    def compute_incomplete_invoice(self):
        domain_incomplete_invoice = self.search(self._get_domain_incomplete_invoice())
        for rec in self:
            if rec in domain_incomplete_invoice:
                rec.incomplete_invoice = True
            else:
                rec.incomplete_invoice = False

    @api.multi
    @api.depends("payment_not_required","payment_bank","payment_date","payment_concept","payment_tre","sale_international")
    def compute_incomplete_payment(self):
        domain_incomplete_payment = self.search(self._get_domain_incomplete_payment())
        for rec in self:
            if rec in domain_incomplete_payment:
                rec.incomplete_payment = True
            else:
                rec.incomplete_payment = False

    @api.multi
    @api.depends("dispatcher_not_required","dispatcher_reference","sale_international")
    def compute_incomplete_dispatcher(self):
        domain_incomplete_dispatcher = self.search(self._get_domain_incomplete_dispatcher())
        for rec in self:
            if rec in domain_incomplete_dispatcher:
                rec.incomplete_dispatcher = True
            else:
                rec.incomplete_dispatcher = False

    @api.multi
    @api.depends("shipping_license_not_required","shipping_license_channel","shipping_license_number",
                 "shipping_license_official_date","estimated_shipping_date","sale_international")
    def compute_incomplete_license(self):
        domain_incomplete_license = self.search(self._get_domain_incomplete_license())
        for rec in self:
            if rec in domain_incomplete_license:
                rec.incomplete_license = True
            else:
                rec.incomplete_license = False

    @api.multi
    @api.depends("booking_not_required","booking_conveyance_id","booking_ETD_date","booking_ETA_date",
                 "booking_transport_company","sale_international")
    def compute_incomplete_booking(self):
        domain_incomplete_booking = self.search(self._get_domain_incomplete_booking())
        for rec in self:
            if rec in domain_incomplete_booking:
                rec.incomplete_booking = True
            else:
                rec.incomplete_booking = False

    @api.multi
    @api.depends("transport_doc_not_required","transport_doc_documents","transport_doc_date","sale_international")
    def compute_incomplete_documents(self):
        domain_incomplete_documents = self.search(self._get_domain_incomplete_documents())
        for rec in self:
            if rec in domain_incomplete_documents:
                rec.incomplete_documents = True
            else:
                rec.incomplete_documents = False

    @api.multi
    @api.depends("certificate_of_analysis_not_required","certificate_of_analysis_shipment_date_to_customer","sale_international")
    def compute_incomplete_certificate_of_analysis(self):
        domain_incomplete_certificate_of_analysis = self.search(self._get_domain_incomplete_certificate_of_analysis())
        for rec in self:
            if rec in domain_incomplete_certificate_of_analysis:
                rec.incomplete_certificate_of_analysis = True
            else:
                rec.incomplete_certificate_of_analysis = False

    @api.multi
    @api.depends("origin_not_required","origin_reference","origin_shipment_date","sale_international")
    def compute_incomplete_origin(self):
        domain_incomplete_origin = self.search(self._get_domain_incomplete_origin())
        for rec in self:
            if rec in domain_incomplete_origin:
                rec.incomplete_origin = True
            else:
                rec.incomplete_origin = False

    @api.multi
    @api.depends("expenses_not_required","expenses_dispatcher_fees","expenses_expenses","sale_international")
    def compute_incomplete_expenses(self):
        domain_incomplete_expenses = self.search(self._get_domain_incomplete_expenses())
        for rec in self:
            if rec in domain_incomplete_expenses:
                rec.incomplete_expenses = True
            else:
                rec.incomplete_expenses = False
    
    @api.multi
    @api.depends("quotation_not_required","quotation_number","quotation_date","quotation_client","sale_international")
    def compute_incomplete_quotation(self):
        domain_incomplete_quotation = self.search(self._get_domain_incomplete_quotation())
        for rec in self:
            if rec in domain_incomplete_quotation:
                rec.incomplete_quotation = True
            else:
                rec.incomplete_quotation = False

    @api.multi
    @api.depends("order_type_foreign","sale_international","incomplete_confirmation","incomplete_proform",
                 "incomplete_invoice","incomplete_payment","incomplete_dispatcher","incomplete_license",
                 "incomplete_booking","incomplete_documents","incomplete_certificate_of_analysis",
                 "incomplete_origin","incomplete_expenses","incomplete_quotation","sale_international")
    def compute_incomplete_traking_order_data(self):
        """
            To determine the set of sales orders that are in an incomplete state,
            we first verify that the sales order is a sale abroad and then
            that any of the conditions raised are not met.
        """
        domain_incomplete_traking_order_data = [
            '&', ('sale_international', '=', True),
            '|', '|', '|', '|', '|', '|', '|', '|', '|', '|',
            ('incomplete_confirmation', '=', True),
            ('incomplete_proform', '=', True),
            ('incomplete_invoice', '=', True),
            ('incomplete_payment', '=', True),
            ('incomplete_dispatcher', '=', True),
            ('incomplete_license', '=', True),
            ('incomplete_booking', '=', True),
            ('incomplete_documents', '=', True),
            ('incomplete_certificate_of_analysis', '=', True),
            ('incomplete_origin', '=', True),
            ('incomplete_expenses', '=', True),
            ('incomplete_quotation', '=', True),
        ]

        incomplete_orders = self.search(domain_incomplete_traking_order_data)
        for rec in self:
            if rec in incomplete_orders:
                rec.incomplete_traking_order_data = True
            else:
                rec.incomplete_traking_order_data = False