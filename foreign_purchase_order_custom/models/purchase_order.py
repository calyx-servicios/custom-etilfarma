import re
import pytz
from datetime import datetime
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    payment_date = fields.Date(string="Payment Date", compute="_compute_payment_fields")

    @api.multi
    def _compute_payment_fields(self):
        
        """ To form the computed fields we must necessarily 
        go through all the invoices and in turn payments 
        that are associated with the purchase order """

        for rec in self:            
            payment_tte_amount = 0
            payment_application_numbers = ''
            payment_bank_and_account = ''
            payment_journal_type = ''
            payment_communication = ''
            payment_date = ''
            payment_reference = ''
            payment_concept = []
            payment_TC = ''
            payment_currency = []
            invoices = rec.invoice_ids
            for invoice in invoices:
                payment_currency.append(invoice.currency_id.name)
                payment_tte_amount += invoice.amount_total_signed - invoice.residual_signed
                payments = invoice.payment_group_ids
                for payment in payments:
                    payment_application_numbers += (payment.display_name + '  ')
                    payment_date += (payment.payment_date + '  ')
                    if payment.notes:
                        payment_reference += (payment.notes + '  ')
                    imputed_vouchers = payment.matched_move_line_ids
                    for imputed_voucher in imputed_vouchers:
                        payment_concept.append(imputed_voucher.invoice_id.display_name)
                    # We extract the exchange rate information from each of the payment 
                    # lines that was made in each payment group.
                    payments_line = payment.payment_ids
                    for payment_line in payments_line:
                        payment_TC += (payment_line.name + '   ')
                        payment_TC += (str(payment_line.amount) + ' ')
                        payment_TC += (str(payment_line.currency_id.name) + ' - ')
                        payment_TC += ('T/C ' + str(payment_line.exchange_rate) + '\r' + '\n')

                
                payment_ids = invoice.payment_ids
                for payment_id in payment_ids:
                    payment_bank_and_account += (payment_id.journal_id.name + '  ')
                    payment_journal_type += (payment_id.journal_id.type + ' ')
                    if payment_id.communication:
                        payment_communication += (payment_id.communication + '  ')

            rec.payment_application_number = payment_application_numbers
            rec.payment_TTE_amount = payment_tte_amount
            rec.payment_date = payment_date
            rec.payment_journal_type = payment_journal_type
            rec.payment_bank_and_account = payment_bank_and_account
            rec.payment_communication = payment_communication
            rec.payment_reference = payment_reference
            rec.payment_concept = rec._get_invoices_list(payment_concept)
            rec.payment_currency = rec._get_currency_payment_list(payment_currency)
            rec.payment_TC = payment_TC