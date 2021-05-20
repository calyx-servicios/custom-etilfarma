# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models, api, _
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import re

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def _default_order_type(self):
        return self.env["sale.order.type"].search([
            ("name", "=", "SOL")
        ], limit=1).id

    def _default_payment_instructions(self):
        return self.env["sale.payment.instructions"].search(
            [("payment_instructions", "!=", "")
        ], limit=1).id

    def _compute_partner_default_bank(self):
        self.payment_bank = self.partner_id.default_bank.bank_id.name

    def _get_invoices_list(self, invoice_list):
        """ It returns the elements of the 
            list that are not repeated """
        invoice_list_sorted = sorted(invoice_list)
        string_list_invoice = ''
        previous_item = ''
        for invoice in invoice_list_sorted:
            if invoice != previous_item:
                string_list_invoice += invoice
            previous_item = invoice

        return string_list_invoice

    @api.multi
    def _compute_payment_fields(self):
        """ To form the computed fields we must necessarily 
        go through all the invoices and in turn payments 
        that are associated with the sales order """
        for rec in self:            
            payments_tre = ''
            payment_date = ''
            payment_concept = []
            payment_exchange_rate = ''
            invoices = rec.invoice_ids
            for invoice in invoices:
                payments = invoice.payment_group_ids
                for payment in payments:
                    payments_tre += (payment.display_name + '  ')
                    payment_date += (payment.payment_date + '  ')
                    imputed_vouchers = payment.matched_move_line_ids
                    for imputed_voucher in imputed_vouchers:
                        payment_concept.append(imputed_voucher.invoice_id.display_name)
                    # We extract the exchange rate information from each of the payment 
                    # lines that was made in each payment group.
                    payments_line = payment.payment_ids
                    for payment_line in payments_line:
                        payment_exchange_rate += (payment_line.name + '   ')
                        payment_exchange_rate += (str(payment_line.amount) + ' ')
                        payment_exchange_rate += (str(payment_line.currency_id.name) + ' - ')
                        payment_exchange_rate += ('T/C ' + str(payment_line.exchange_rate) + '\r' + '\n')

            rec.payment_tre = payments_tre
            rec.payment_date = payment_date
            rec.payment_concept = self._get_invoices_list(payment_concept)
            rec.payment_exchange_rate = payment_exchange_rate


    proforma_not_required = fields.Boolean(string="Proforma Not Required")

    order_type_foreign = fields.Boolean(string="Foreign Order", default=False)

    incoterm_id = fields.Many2one(
        comodel_name='stock.incoterms', string='Incoterm')

    shipment_id = fields.Many2one(
        comodel_name="sale.shipment", string="Shipment",
    )

    certificate_of_analysis = fields.Char(string='Certificate of Analysis')
    

    payment_instructions_id = fields.Many2one(
        comodel_name="sale.payment.instructions",
        string="Payment instructions",
        default=_default_payment_instructions,
    )

    place_of_delivery_id = fields.Many2one(
        comodel_name="sale.delivery", string="Place of Delivery",
    )

    term_payments = fields.Many2one(
        related="payment_term_id",
        string="Terms of Payment",
    )    
    order_type = fields.Many2one(
        comodel_name="sale.order.type",
        readonly=False,
        string="Type",
        ondelete="restrict",
        default=_default_order_type,
    )

    customer_purchase_order = fields.Char(string="Customer Purchase Order")

    estimated_shipping_date = fields.Datetime(string="Estimated Shipping Date")
    observations = fields.Text(string="Observations", size=150)
    carriers = fields.Text(string="Carriers", size=150)

    quotation_not_required = fields.Boolean(string="Quotation Not Required")
    quotation_client = fields.Char(string="Quotation Client", compute="_onchange_update_quotation_client")
    quotation_number = fields.Char(string="Quotation Number", compute="_onchange_update_quotation_number")
    quotation_date = fields.Date(string="Quotation Date", compute="_onchange_update_quotation_date")

    proforma_not_required = fields.Boolean(string="Proforma Not Required")
    proforma_number = fields.Char(string="Proforma Number")
    proforma_date = fields.Date(string="Proforma Date")

    confirmation_not_required = fields.Boolean(string="Confirmation Not Required")
    confirmation_number = fields.Char(string="Confirmation Number")
    date_confirm= fields.Date(string="Confirmation Date")

    certificate_of_analysis_not_required = fields.Boolean(string="Certificate Of Analysis Not Required")
    certificate_of_analysis_shipment_date_to_customer = fields.Date(string="Certificate Of Analysis Shipment Date to Customer")

    invoice_not_required = fields.Boolean(string="Invoice Not Required")
    invoice_number = fields.Char(string="Invoice Number", compute="_get_invoice_number")
    invoice_date = fields.Char(string="Invoice Date", compute="_get_invoice_date")

    payment_not_required = fields.Boolean(string="Payment Not Required")
    payment_bank = fields.Char(string="Payment Bank", compute="_compute_partner_default_bank")
    payment_tre = fields.Char(string="Payment TRE", compute="_compute_payment_fields")
    payment_date = fields.Char(string="Payment Date", compute="_compute_payment_fields")
    payment_concept = fields.Char(string="Payment Concept", compute="_compute_payment_fields")
    payment_exchange_rate = fields.Text("Payment Exchange Rate", compute="_compute_payment_fields")
    payment_transport_company = fields.Char(string="Payment Transport Company")

    dispatcher_not_required = fields.Boolean(string="Dispatcher Not Required")
    dispatcher_id = fields.Many2one(
        comodel_name="sale.dispatcher", string="Dispatcher",
    )
    dispatcher_address = fields.Char(string="Address", related="dispatcher_id.address")
    dispatcher_email = fields.Char(string="Email", related="dispatcher_id.email")
    dispatcher_phone_number = fields.Char(string="Phone Number", related="dispatcher_id.phone_number")
    dispatcher_not_required = fields.Boolean(string="Dispatcher Not Required")
    dispatcher_reference = fields.Char(string="Dispatcher Reference")

    booking_not_required = fields.Boolean(string="Booking Not Required")
    booking_conveyance_id = fields.Many2one(
        comodel_name="sale.booking.conveyance",
        string="Booking Conveyance")    
    booking_ETD_date = fields.Date(string="Booking ETD Date")
    booking_ETA_date = fields.Date(string="Booking ETA Date")
    booking_transport_company = fields.Char(string="Booking Transport Company")

    transport_doc_not_required = fields.Boolean(string="Transport Doc Not Required")
    transport_doc_documents = fields.Char(string="Transport Doc Documents")
    transport_doc_date = fields.Date(string="Transport Doc Date")

    shipping_license_not_required = fields.Boolean(string="Shipping License Not Required")
    shipping_license_number = fields.Char(string="Shipping License Number")
    shipping_license_official_date = fields.Date(string="Shipping License Official Date")
    shipping_license_channel = fields.Char(string="Shipping License Channel")
    ship_name = fields.Char(string='Ship Name')
    
    origin_not_required = fields.Boolean(string="Origin Not Required")
    origin_reference = fields.Char(string="Origin Reference")
    origin_shipment_date = fields.Date(string="Origin Date")

    merchandise_delivery_not_required = fields.Boolean(string="Merchandise Delivery Not Required")
    merchandise_delivery_date = fields.Date(string="Merchandise Delivery Date")

    expenses_not_required = fields.Boolean(string="Expenses Not Required")
    expenses_dispatcher_fees = fields.Char(string="Dispacher Fees")
    expenses_expenses = fields.Char(string="Expenses")

    after_shipment_not_required = fields.Boolean(string="After Shipment Not Required")
    after_shipment_customs_compliance_date = fields.Date(string="After Shipment Customs Compliance Date")
    after_shipment_invoice_closing_date_AFIP = fields.Date(string="After Shipment Invoice Closing Date")
    after_shipment_boarding_permit_date = fields.Date(string="After Shipment Boarding Permit Date")

    sale_code = fields.Char(compute="_onchange_update_sale_code")
    
    @api.constrains('payment_exchange_rate')
    def _check_format_payment_exchange_rate(self):
        for rec in self:
            if rec.payment_exchange_rate:
                match = re.match("^[0-9]+([,][0-9]+)?$", rec.payment_exchange_rate)
                if match == None:
                    raise UserError("exchange rate invalid format")

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
                    raise UserError("expenses invalid format")

    @api.onchange('term_payments')
    def _onchange_update_payment_term_id(self):
        """
            dynamic update of related field 'payment_term_id'
        """
        self.payment_term_id= self.term_payments

    def _get_invoice_date(self):
        for rec in self:
            invoice_date = ''
            invoices = rec.env["account.invoice"].search([('origin', '=',rec.name)])
            for invoice in invoices:
                if invoice.date_invoice:
                    invoice_date += (invoice.date_invoice + '  ')
            rec.invoice_date = invoice_date
    
    def _get_invoice_number(self):
        for rec in self:
            invoice_number = ''
            invoices = rec.env["account.invoice"].search([('origin', '=',rec.name)])
            for invoice in invoices:
                if invoice.display_name:
                    invoice_number += (invoice.display_name + '  ')
                    
            rec.invoice_number = invoice_number

    @api.depends('partner_id')
    def _onchange_update_quotation_client(self):
        """
            dynamic update of related field 'quotation_client'
        """
        self.quotation_client= self.partner_id.name

    @api.depends('name')
    def _onchange_update_quotation_number(self):
        """
            dynamic update of related field 'quotation_number'
        """
        for rec in self:
            rec.quotation_number= rec.name

    @api.depends('date_order')
    def _onchange_update_quotation_date(self):
        """
            dynamic update of related field 'quotation_date'
        """
        if self.date_order:
            self.quotation_date = datetime.strptime(self.date_order, "%Y-%m-%d %H:%M:%S")
        
    def _set_comfirmation(self):
        for rec in self:
            if rec.state in "sale" and self.confirmation_date and not self.date_confirm:
                rec.confirmation_number= "COE" + ''.join(filter(str.isdigit, rec.name))
                rec.date_confirm = datetime.strptime(rec.confirmation_date, "%Y-%m-%d %H:%M:%S")    

    def _set_proforma(self):
        for rec in self:
            if rec.state in "draft" or not rec.proforma_date:
                rec.proforma_number= "PRE" + ''.join(filter(str.isdigit, rec.name))
                rec.proforma_date= fields.Datetime.now()

    @api.depends('name')
    def _onchange_update_sale_code(self):
        code = ''.join(filter(str.isdigit, self.name))
        if self.order_type.foreign_order:
            code = "E " + code
        else: 
            code = "L " + code
        self.sale_code = code

    @api.onchange('payment_term_id')
    def _onchange_update_term_payments(self):
        """
            dynamic update of related field 'term_payments'
        """
        self.term_payments= self.payment_term_id    

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        When the partner changes, we get the order_type
        from the partner sale_type field if this has
        a value
        """
        super().onchange_partner_id()
        sale_type = (
            self.partner_id.sale_type
            or self.partner_id.commercial_partner_id.sale_type
        )
        if sale_type:
            self.order_type = sale_type

    @api.multi
    @api.onchange("order_type")
    def onchange_order_type(self):
        """
        When the order types changes, we get the incoterm from
        the order type record if this has a value.
        """
        for order in self:
            if order.order_type.incoterm_id:
                order.incoterm_id = order.order_type.incoterm_id.id

        for record in self:
            if record.order_type:
                if record.order_type.foreign_order:
                    record.order_type_foreign = True
                else:
                    record.order_type_foreign = False
            else:
                record.order_type_foreign = False

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self._set_comfirmation()
        return res

    @api.model
    def create(self, vals):
        """
        Adding the prefix number of the sequence selected
        in the sale type.
        """
        if vals.get("name", "/") == "/" and vals.get("order_type"):
            sale_type = self.env["sale.order.type"].browse(
                vals["order_type"]
            )
            if sale_type.sequence_id:
                vals["name"] = sale_type.sequence_id.next_by_id()
        return super().create(vals)

    @api.multi
    def print_sale_foreign_report(self):
        if self.state == "draft":
            self.write({"state": "sent"})
        return self.env.ref(
            "foreign_trade.action_foreign_sale_report"
        ).report_action(self)

    @api.multi
    def action_sfo_send(self):
        """
        This function opens a window to compose an email, with the edi
        table template message loaded by default
        and the sale foreign report as attachment
        """
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_id = ir_model_data.get_object_reference(
                "foreign_trade",
                "email_template_foreign_sale",
            )[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "default_model": "sale.order",
                "default_res_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "sale.mail_template_data_notification_email_sale_order",
                "force_email": True,
            }
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }

    @api.multi
    def print_foreign_sale_proforma_report(self):
        self._set_proforma()
        if self.state == "draft":
            self.write({"state": "sent"})
        return self.env.ref(
            "foreign_trade.action_foreign_sale_proforma_report"
        ).report_action(self)

    @api.multi
    def action_proforma_send(self):
        """
        This function opens a window to compose an email, with the edi
        able template message loaded by default
        and the proforma report as attachment
        """
        self._set_proforma()
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_id = ir_model_data.get_object_reference(
                "foreign_trade",
                "email_template_foreign_sale_proforma",
            )[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "default_model": "sale.order",
                "default_res_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "sale.mail_template_data_notification_email_sale_order",
                "force_email": True,
            }
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }