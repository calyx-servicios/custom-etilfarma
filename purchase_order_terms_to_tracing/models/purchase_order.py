from odoo import models, fields

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    client_tracing = fields.Text('Internal Client Tracing')