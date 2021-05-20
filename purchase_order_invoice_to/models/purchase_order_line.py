from odoo import fields, models, api, _
from odoo.exceptions import UserError

class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    confirm_product = fields.Boolean("Comfirm Product")
    purchase_order_created = fields.Boolean("Create Order")
    tracked_line = fields.Boolean("Tracked",default=True)
    product_id_origin = fields.Integer("Product ID")