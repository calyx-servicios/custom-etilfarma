from odoo import fields, models, api, _


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    """
        I added this functionality here to avoid to get this behavior in 
        other situations. Basicaly the Client requests to maintain 
        the same currency on the Invoice from the PO where it is
        created from.
    """

    @api.model
    def default_get(self, field_list):
        res = super(AccountInvoice, self).default_get(field_list)
        currency = self.env['purchase.order'].browse(self._context.get('active_ids')).currency_id.id
        res.update({
            'currency_id': currency
        })
        return res