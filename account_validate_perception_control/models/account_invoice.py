from odoo import fields, models, api, _
from odoo.exceptions import UserError, ValidationError

class AccountInvoice(models.Model):
    _inherit = "account.invoice"
            
    button_clicked = fields.Boolean(string='Button clicked')

    @api.multi
    def control_perception(self):
        self.button_clicked = True
        res = super(AccountInvoice, self).control_perception()
        return res 
    
    
    @api.multi
    def action_invoice_open(self):
        val = super(AccountInvoice, self).action_invoice_open()
        if not self.button_clicked:
            raise ValidationError(_('The perception control was not run'))
        return val 
