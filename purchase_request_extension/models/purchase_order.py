from odoo import api, fields, models


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    """ 
        This field is created for View Readonly Logic
    """
    from_purchase_request_line = fields.Boolean(string="Created from Purchase Request Line", default=False)

    @api.model
    def default_get(self, fields):
        """
            In this case when a Purchase Order is created from Purchase Request App,
            it will have the Date Planned field as Readonly.
        """
        rec = super(PurchaseOrder, self).default_get(fields)
        if self.env.context.get('active_model', False) == 'purchase.request.line':
            rec['from_purchase_request_line'] = True
        return rec
