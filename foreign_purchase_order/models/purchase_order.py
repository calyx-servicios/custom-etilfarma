# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import re
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError

def _format_date(date_utc_format):
    """Change the UTC format used by Odoo for dd/mm/yyyy

    Arguments:
        date_utc_format {str} -- Date UTC format yyyy/mm/dd

    Returns:
        str -- Date in dd/mm/yyyy format.
    """
    if date_utc_format:
        date_d_m_y_format = datetime.strptime(date_utc_format.split(" ")[0], '%Y-%m-%d').strftime('%d/%m/%Y')
        return date_d_m_y_format
    else:
        return False


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_type_foreign = fields.Boolean(string="Foreign Order", default=False)

    purchase_sample = fields.Boolean(string="Sample?", default=False)

    delivery_date_planned = fields.Date(string="Delivery Date Planned")

    customer_purchase_order = fields.Char(string="Customer Purchase Order")

    place_of_delivery_id = fields.Many2one(
        comodel_name="purchase.delivery", string="Place of Delivery",
    )

    packaging_id = fields.Many2one(
        comodel_name="purchase.packaging", string="Packaging",
    )

    delivery_date_week = fields.Char(
        string="Delivery Date (Week)",
        compute="_compute_delivery_date_week",
        store=True,
    )

    send_documents_to = fields.Text(string="Send documents to",)

    def _get_company_child_ids(self):
        company_child_ids = self.env.user.company_id.partner_id.child_ids.ids
        return [('id', 'in', company_child_ids)]

    use_other_company_address = fields.Many2one(
        string="Use another company Address?",
        comodel_name="res.partner",
        domain=_get_company_child_ids)

    shipment_id = fields.Many2one(
        comodel_name="purchase.shipment", string="Shipment",
    )
    import_license_id = fields.Many2one(
        comodel_name="purchase.import.license", string="Import License",
    )
    certificate_of_analysis_id = fields.Many2one(
        comodel_name="purchase.certificate.analysis",
        string="Certificate of Analysis",
    )

    p_o = fields.Char(
        string="P/O",
        related="customer_purchase_order"
    )

    packing_list_id = fields.Many2one(
        comodel_name="purchase.packing.list", string="Packing List",
    )
    term_payments = fields.Many2one(
        related="payment_term_id",
        string="Payment Conditions",
    )

    extra_notes = fields.Text(string="Extra", size=150)

    description = fields.Char(string="Description",
                              compute="_compute_description",
                              store=True,)

    confirmation_number = fields.Char(string="Confirmation Number")
    confirmation_date = fields.Date(string="Confirmation Date")
    confirmation_not_required = fields.Boolean(string="Confirmation Not Required")

    proforma_number = fields.Char(string="Proforma Number")
    proforma_date = fields.Date(string="Proforma Date")
    proforma_not_required = fields.Boolean(string="Proforma Not Required")

    payment_bank = fields.Text(string="Payment Bank")
    payment_account = fields.Char(string="Payment Account")
    payment_application_number = fields.Char(string="Payment Application number")
    payment_date = fields.Date(string="Payment Date")
    payment_reference = fields.Char(string="Payment Reference")
    payment_concept = fields.Text(string="Payment Concept")
    payment_TTE_amount = fields.Char(string="Payment TTE Amount")
    payment_TC = fields.Char(string="Payment TC")
    payment_currency = fields.Selection([ ("ARS", "ARS"),("EUR", "EUR"),("USD", "USD")], default="USD", string="Payment Currency")
    payment_not_required = fields.Boolean(string="Payment Not Required")

    dispatcher_reference = fields.Char(string="Dispatcher Reference")
    dispatcher_not_required = fields.Boolean(string="Dispatcher Not Required")

    intervention_reference = fields.Char(string="Intervention Reference")
    intervention_VPE_amount = fields.Char(string="Intervention VPE Amount")
    intervention_application_date = fields.Date(string="Intervention Application Date")
    intervention_approval_date = fields.Date(string="Intervention Approval Date")
    intervention_not_required = fields.Boolean(string="Intervention Not Required")

    import_license_reference = fields.Char(string="Import License Reference")
    import_license_approval_date = fields.Date(string="Import License Approval Date")
    import_license_official_date = fields.Date(string="Import License Official Date")
    import_license_not_required = fields.Boolean(string="Import License Not Required")
 
    booking_conveyance_id = fields.Many2one(
        comodel_name="purchase.booking.conveyance",
        string="Booking Conveyance")
    booking_origin = fields.Char(string="Booking Origin")
    booking_ETD_date = fields.Date(string="Booking ETD Date")
    booking_ETA_date = fields.Date(string="Booking ETA Date")
    booking_transport_company = fields.Char(string="Booking Transport Company")
    booking_not_required = fields.Boolean(string="Booking Not Required")

    documents_commercial_invoice_number = fields.Char(string="Documents Comercial Invoice Number",
                                                      compute='_compute_commercial_invoice_number',
                                                      store=True)
    documents_FC_date = fields.Date(string="Documents FC Date",
                                    compute='_compute_documents_fc_date',
                                    store=True)
    documents_quality_certificate_approval_date = fields.Date(string="Documents Certificate of Analysis Approval Date")
    documents_shipping_document = fields.Char(string="Documents Shipping Document")
    documents_shipping_date = fields.Date(string="Documents Shipping Date")
    documents_date_shipment_originals = fields.Date(string=("Date of shipment of originals to dispatcher"))
    documents_not_required = fields.Boolean(string="Documents Not Required")

    delivery_number = fields.Char(string="Import Delivery Number")
    delivery_official_date = fields.Date(string="Import Official Delivery Date")
    delivery_chanel_id = fields.Many2one(
        comodel_name="purchase.delivery.chanel",
        string="Delivery Chanel")
    delivery_not_required = fields.Boolean(string="Delivery Not Required")

    original_documentation_original_receipt_date = fields.Date(string="Original Documentation Original Receipt Date")
    original_documentation_not_required = fields.Boolean(string="Original Documentation Not Required")

    expenses_dispatcher_fees = fields.Char(string="Expenses dispatcher Fees")
    expenses_expenses = fields.Char(string="Expenses")
    expenses_not_required = fields.Boolean(string="Expenses Not Required")

    @api.constrains('intervention_VPE_amount')
    def _check_format_intervention_VPE_amount(self):
        for rec in self:
            if rec.intervention_VPE_amount:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.intervention_VPE_amount)
                if match == None:
                    raise UserError("VPE Amount invalid format")
            
    @api.constrains('payment_TTE_amount')
    def _check_format_payment_TTE_amount(self):
        for rec in self:
            if rec.payment_TTE_amount:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.payment_TTE_amount)
                if match == None:
                    raise UserError("TEE Amount invalid format")
    
    @api.constrains('payment_TC')
    def _check_format_payment_TC(self):
        for rec in self:
            if rec.payment_TC:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.payment_TC)
                if match == None:
                    raise UserError("TC Amount invalid format")
    
    @api.constrains('expenses_dispatcher_fees')
    def _check_format_expenses_dispatcher_fees(self):
        for rec in self:
            if rec.expenses_dispatcher_fees:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.expenses_dispatcher_fees)
                if match == None:
                    raise UserError("Dispatcher fees invalid format")

    @api.constrains('expenses_expenses')
    def _check_format_expenses_expenses(self):
        for rec in self:
            if rec.expenses_expenses:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.expenses_expenses)
                if match == None:
                    raise UserError("Expenses invalid format")

    @api.onchange('term_payments')
    def _onchange_update_payment_term_id(self):
        """
            dynamic update of related field 'payment_term_id'
        """
        self.payment_term_id= self.term_payments

    @api.onchange('payment_term_id')
    def _onchange_update_term_payments(self):
        """
            dynamic update of related field 'term_payments'
        """
        self.term_payments= self.payment_term_id    

    @api.onchange("confirmation_not_required")
    def _onchange_confirmation_not_required(self):
        self.confirmation_number = ""
        self.confirmation_date = ""

    @api.onchange("proforma_not_required")
    def _onchange_proforma_not_required(self):
        self.proforma_number = ""
        self.proforma_date = ""

    @api.onchange("payment_not_required")
    def _onchange_payment_not_required(self):
        self.payment_bank = ""
        self.payment_concept = ""
        self.payment_application_number = ""
        self.payment_account = ""
        self.payment_date = ""
        self.payment_reference = ""
        self.payment_TC = ""
        self.payment_TTE_amount = ""
        self.payment_currency = ""

    @api.onchange("dispatcher_not_required")
    def _onchange_dispatcher_not_required(self):
        self.dispatcher_reference = ""

    @api.onchange("intervention_not_required")
    def _onchange_intervention_not_required(self):
        self.intervention_application_date = ""
        self.intervention_approval_date = ""
        # self.intervention_reference = "" # Line commented because of autocomplete Interventions Type behavior.
        self.intervention_VPE_amount = ""

    @api.onchange("import_license_not_required")
    def _onchange_import_license_not_required(self):
        self.import_license_approval_date = ""
        self.import_license_id = ""
        self.import_license_official_date = ""
        self.import_license_reference = ""

    @api.onchange("booking_not_required")
    def _onchange_booking_not_required(self):
        self.booking_conveyance_id = ""
        self.booking_ETA_date = ""
        self.booking_ETD_date = ""
        self.booking_origin = ""
        self.booking_transport_company = ""

    @api.onchange("documents_not_required")
    def _onchange_documents_not_required(self):
        self.documents_commercial_invoice_number = ""
        self.documents_FC_date = ""
        self.documents_quality_certificate_approval_date = ""
        self.documents_shipping_date = ""
        self.documents_shipping_document = ""

    @api.onchange("delivery_not_required")
    def _onchange_delivery_not_required(self):
        self.delivery_chanel_id = ""
        self.delivery_date_week = ""
        self.delivery_number = ""
        self.delivery_official_date = ""

    @api.onchange("original_documentation_not_required")
    def _onchange_original_documentation_not_required(self):
        self.original_documentation_original_receipt_date = ""

    @api.onchange("expenses_not_required")
    def _onchange_expenses_not_required(self):
        self.expenses_dispatcher_fees = ""
        self.expenses_expenses = ""
    
    @api.onchange("order_line")
    def _onchange_order_line(self):
        intervention_reference = []
        not_duplicated_intervention = []
        for line in self.order_line:
            intervention_reference.append(line.intervention_types)
        for intervention in intervention_reference:
            if intervention not in not_duplicated_intervention:
                not_duplicated_intervention.append(intervention)
        self.intervention_reference = " ".join(not_duplicated_intervention) 
            

    @api.depends('invoice_ids')
    def _compute_commercial_invoice_number(self):
        """
            In case Document Commercial Invoice Number is empty
            we write the Invoice Number of the First (index -1) Invoice
            related created.
            Same for Document FC Date.
        """
        for record in self:
            if not record.documents_commercial_invoice_number:
                if record.invoice_ids:
                    record.documents_commercial_invoice_number = record.invoice_ids[-1].document_number

    @api.depends('invoice_ids.date_invoice')
    def _compute_documents_fc_date(self):
        for record in self:
            if not record.documents_FC_date:
                if record.invoice_ids:
                    record.documents_FC_date = record.invoice_ids[-1].date_invoice

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """
            When the order type changes, check if that order is a foreign order
            if it is, then set like True the variable order_type_foreign
            to show some fields in the purchase view.
        """
        for record in self:
            if record.order_type:
                if record.order_type.foreign_order:
                    record.order_type_foreign = True
                else:
                    record.customer_purchase_order = ""
                    record.order_type_foreign = False

            else:
                record.customer_purchase_order = ""
                record.order_type_foreign = False

    @api.onchange('order_line')
    def _onchange_order_line(self):
        interventions = []
        for record in self:
            for line in record.order_line:
                for intervention in line.product_id.intervention_types:
                    if intervention.name not in interventions:
                        interventions.append(intervention.name)

            interventions_to_write = " "
            record.intervention_reference = interventions_to_write.join(interventions)

    @api.depends('order_line')
    def _compute_description(self):
        for record in self:
            """ To Write in Description field, used in List View """
            if len(record.order_line.ids) == 1:
                record.description = record.order_line[0].product_tmpl_id.display_name
            elif len(record.order_line.ids) > 1:
                record.description = "Mix"

    @api.onchange("use_other_company_address")
    def _onchange_use_other_company_address(self):
        """

        """
        for record in self:
            if self.use_other_company_address:
                self._write_other_company_document_to(record.use_other_company_address)
            if not self.use_other_company_address:
                self._write_other_company_document_to(record.company_id)

    def _write_other_company_document_to(self, record):
        info_to_write = ""

        if record.name:
            info_to_write += _("%s\n==========\n") % record.name
        if record.street:
            info_to_write += _("Street: %s\n") % record.street
        if record.zip:
            info_to_write += _("Zip Code: %s\n") % record.zip
        if record.state_id:
            info_to_write += _("State: %s\n") % record.state_id.name
        if record.country_id:
            info_to_write += _("Country: %s\n") % record.country_id.name
        if record.main_id_number:
            info_to_write += "CUIT: {}\n".format(record.main_id_number)

        self.send_documents_to = info_to_write

    @api.depends("date_planned")
    def _compute_delivery_date_week(self):
        """
        We take the date_planned assigned by the user to
        format it into the regular format.
        Then we concatenate a string with that formmated
        date plus the week number
        """
        for po in self:
            if po.date_planned:
                date_fmt = "/".join(
                    reversed(po.date_planned.split(" ")[0].split("-"))
                )
                po.delivery_date_week = "{} - W{}".format(
                    date_fmt,
                    datetime.strptime(
                        po.date_planned, "%Y-%m-%d %H:%M:%S"
                    ).isocalendar()[1],
                )

    @api.onchange("purchase_sample")
    def _onchange_purchase_sample(self):
        """
        When the purchase_sample is True, we get the purchase sample type
        and set in the purchase_type field,
        however if the purchase_sample is false, we get the purchase type
        in the partner and set in purchase_type field.
        """
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        ocl = self.env.ref("purchase_order_types.po_type_regular")
        purchase_type = (
            self.partner_id.purchase_type
            or self.partner_id.commercial_partner_id.purchase_type
        )
        for record in self:
            if ocm:
                if record.purchase_sample:
                    record.order_type = ocm.id
                    if ocm.foreign_order:
                        record.order_type_foreign = True
                else:
                    if purchase_type:
                        record.order_type = purchase_type

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        When the partner change and if purchase_sample it is true
        then the order_type keeps in ocm
        """
        super().onchange_partner_id()
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        if self.purchase_sample:
            self.order_type = ocm.id

    def _get_invoiced(self):
        """
         Inherit to force sample POs to be in 'Nothing to Bill' state
        """
        super(PurchaseOrder, self)._get_invoiced()
        for order in self.filtered(
            lambda po: po.purchase_sample and po.invoice_status == "to invoice"
        ):
            order.invoice_status = "no"

    @api.multi
    def _get_default_special_indications(self):
        """
         Set the Special Indications based on the value of the
         field in Purchase settings
        """
        icpsudo = self.env[
            "ir.config_parameter"
        ].sudo()  # icpsudo -> Ir.Config_Parameter access with sudo()
        indications = icpsudo.get_param(
            "foreign_purchase_order.special_indications"
        )
        return indications

    special_indications = fields.Text(
        string="Special Indications", default=_get_default_special_indications
    )

    """ Fields and Method used to update the status of information to display at List View """
    confirmation_status = fields.Char(string='Confirmation', compute='_compute_tracking_status', store=True)
    proforma_status = fields.Char(string='Proform', compute='_compute_tracking_status', store=True)
    payment_TTE_status = fields.Char(string='Payment', compute='_compute_tracking_status', store=True)
    booking_conveyance_status = fields.Char(string='Booking Conveyance', compute='_compute_tracking_status', store=True)
    booking_transport_company_status = fields.Char(string='Booking Transport', compute='_compute_tracking_status', store=True)
    booking_ETD_date_status = fields.Char(string='Booking ETD', compute='_compute_tracking_status', store=True)
    booking_ETA_date_status = fields.Char(string='Booking ETA', compute='_compute_tracking_status', store=True)
    documents_commercial_invoice_number_status = fields.Char(string='Document Commercial Invoice', compute='_compute_tracking_status', store=True)
    documents_shipping_document_status = fields.Char(string='Shipping Document', compute='_compute_tracking_status', store=True)
    delivery_number_status = fields.Char(string='Delivery', compute='_compute_tracking_status', store=True)
    reception_status = fields.Char(string='Reception', compute='_compute_reception_status', store=True)

    @api.depends('confirmation_not_required', 'proforma_not_required', 'payment_not_required',
                 'booking_not_required', 'documents_not_required', 'delivery_not_required',
                 'confirmation_number', 'proforma_number', 'payment_TTE_amount', 'booking_conveyance_id',
                 'booking_transport_company', 'booking_ETD_date', 'booking_ETA_date', 'documents_commercial_invoice_number',
                 'documents_shipping_document', 'delivery_number')
    def _compute_tracking_status(self):

        for record in self:
            if record.confirmation_not_required:
                record.confirmation_status = _("Not required")
            else:
                record.confirmation_status = record.confirmation_number

            if record.proforma_not_required:
                record.proforma_status = _("Not required")
            else:
                record.proforma_status = record.proforma_number

            if record.payment_not_required:
                record.payment_TTE_status = _("Not required")
            else:
                record.payment_TTE_status = record.payment_TTE_amount

            if record.booking_not_required:
                record.booking_conveyance_status = _("Not required")
                record.booking_transport_company_status = _("Not required")
                record.booking_ETD_date_status = _("Not required")
                record.booking_ETA_date_status = _("Not required")
            else:
                record.booking_conveyance_status = record.booking_conveyance_id.booking_conveyance
                record.booking_transport_company_status = record.booking_transport_company
                record.booking_ETD_date_status = _format_date(record.booking_ETD_date)
                record.booking_ETA_date_status = _format_date(record.booking_ETA_date)

            if record.documents_not_required:
                record.documents_commercial_invoice_number_status = _("Not required")
                record.documents_shipping_document_status = _("Not required")
            else:
                record.documents_commercial_invoice_number_status = record.documents_commercial_invoice_number
                record.documents_shipping_document_status = record.documents_shipping_document

            if record.delivery_not_required:
                record.delivery_number_status = _("Not required")
            else:
                record.delivery_number_status = record.delivery_number

    @api.depends('picking_ids', 'picking_ids.state')
    def _compute_reception_status(self):
        for record in self:
            if record.picking_ids and all([x.state in ['done', 'cancel'] for x in record.picking_ids]):
                record.reception_status = _format_date(record.picking_ids[-1].scheduled_date)
            else:
                record.reception_status = _('Pending')


class InterventionReferences(models.Model):
    _name = "purchase.order.interventions"

    name = fields.Char(string='Name', required=True)