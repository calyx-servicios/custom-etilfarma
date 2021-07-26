<<<<<<< HEAD
from odoo import fields, models, api
=======
from odoo import fields, models, api, http, _
from odoo.exceptions import UserError

>>>>>>> 37d399f30e4058188c01558b92107a832dd65fa2

class StockPicking(models.Model):
    _inherit = "stock.move.line"
        
    voucher_ids = fields.One2many(
        'stock.picking.voucher',
        'picking_id',
        'Vouchers',
        copy=False,
        related='picking_id.voucher_ids'
    )
    origin = fields.Char(
        string="Source Document",
        related='picking_id.origin'
    )
    partner_id = fields.Many2one(
        'res.partner', 
        'Partner', 
        related='picking_id.partner_id'
    )
    delivery_date = fields.Date(
        string="Delivery date",
    )
    reception_date = fields.Date(
        string="Reception date",
    )
    warehouse_id = fields.Many2one(
        'stock.warehouse', 
        'Warehouse',
        related='picking_id.picking_type_id.warehouse_id'
    )
    picking_type_id = fields.Many2one(
        related='picking_id.picking_type_id',
        store=True,
    )
    picking_type_code = fields.Selection([
        ('incoming', 'Vendors'),
        ('outgoing', 'Customers'),
        ('internal', 'Internal')], 
        related='picking_id.picking_type_id.code',
        readonly=True)
    comments = fields.Char(sring="Comments")
    order_date = fields.Date(string="Order date", 
        related="move_id.order_date",
        store=True
    )
    customer_purchase_order = fields.Char(
        compute="_customer_purchase_order",
        store=True,
    )
    invoice_status = fields.Char(
        compute="_invoice_status",
        store=True,
    )
    shipping_address = fields.Char(
        compute="_compute_address",
        store=True,
    )

    @api.depends("picking_id")
    def _customer_purchase_order(self):
        for record in self:
            if record.picking_id:
                record.customer_purchase_order = record.picking_id.sale_id.customer_purchase_order
            else:
                record.customer_purchase_order = ""

    @api.depends("move_id")
    def _invoice_status(self):
        for record in self:
            if record.move_id:
                if record.move_id.invoice_status == "upselling":
                    record.invoice_status = "Oportunidad de venta adicional"
                elif record.move_id.invoice_status == "invoiced":
                    record.invoice_status = "Totalmente facturado"
                elif record.move_id.invoice_status == "to invoice":
                    record.invoice_status = "A facturar"
                else:
                    record.invoice_status = "Nada a facturar"
            else:
                record.invoice_status = ""

    @api.depends('partner_id')
    def _compute_address(self):
        for record in self:
            address_format = "%(name)s\n %(street)s\n%(street2)s\n%(city)s\n%(state_name)s\n%(country_name)s"
            args = {
                'street': record.partner_id.street,
                'street2': record.partner_id.street2,
                'state_code': record.partner_id.state_id.code or '',
                'state_name': record.partner_id.state_id.name or '',
                'city': record.partner_id.city or '',
                'country_code': record.partner_id.country_id.code or '',
                'zip': record.partner_id.zip or '',
                'country_name': record.partner_id.country_id.display_name,
                'name': record.partner_id.name,
            }
            record.shipping_address = address_format % args
class StockMove(models.Model):
    _inherit = "stock.move"

    order_date = fields.Date(string="Order date", related="sale_line_id.order_date")
    invoice_status = fields.Selection(string="invoice status", related="sale_line_id.invoice_status")

    name = fields.Char(index=True)
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='invoice',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")
    street = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    city = fields.Char()
    zip = fields.Char()
    street2 = fields.Char()
    
    @api.depends('origin')
    def get_link_action(self):
        base_url = base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
        
        sales_prefix_ids = self.env['ir.sequence'].search([('sale_seq','=',True)])
        sale_prefixes = []
        for x in sales_prefix_ids:
            sale_prefixes.append(x.prefix)
        
        purchase_prefix_ids = self.env['ir.sequence'].search([('purchase_seq','=',True)])
        purchase_prefixes = []
        for x in purchase_prefix_ids:
            purchase_prefixes.append(x.prefix)
        if self.origin:
            if any(prefix in self.origin for prefix in sale_prefixes):
                sales_action_id = self.env.ref('sale.action_quotations')
                sales_move_id = self.env['sale.order'].search([('name','=',self.origin)])
                return {
                    "type": "ir.actions.act_url",
                    "url" : "%s/web#id=%s&view_type=form&model=sale.order&action=%s" % 
                    (base_url,sales_move_id.id,sales_action_id.id),
                    "target" : "new"
                }
                
            elif any(prefix in self.origin for prefix in purchase_prefixes):
                purchase_action_id = self.env.ref('purchase.purchase_form_action')
                purchase_move_id = self.env['purchase.order'].search([('name','=',self.origin)])
                return {
                    "type": "ir.actions.act_url",
                    "url" : "%s/web#id=%s&view_type=form&model=purchase.order&action=%s" % 
                    (base_url,purchase_move_id.id,purchase_action_id.id),
                    "target" : "new"
                }
            else:
                raise UserError(_('Can only view sale or purchase orders'))
        else:
            raise UserError(_('Move has no origin'))
