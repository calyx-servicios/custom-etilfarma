from odoo import fields, models, api, http

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


    @api.multi
    def get_link(self):
        def get_move(records,origin):
            for line in records:
                if line.name == origin:
                    return line.id
        base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
        # If move is purchase
        purchase_action_id = self.env.ref('	purchase.purchase_form_action')
        purchase_menu_id = self.env.ref('purchase.menu_purchase_form_action')
        purchase_move_ids = self.env['purchase.order'].search([])
        # If move is sale
        sales_action_id = self.env.ref('sale.action_quotations')
        sales_menu_id = self.env.ref('sale.menu_sale_quotations')
        sales_move_ids = self.env['sale.order'].search([])
        for line in self:
            if line.origin_sale:
                move_id = get_move(sales_move_ids,line.origin)
                line.url = '%s/web#id=%s&view_type=form&model=sale.order&menu_id=%s&action=%s'%(base_url,move_id,sales_menu_id.id,sales_action_id.id)
            if line.origin_purchase:
                move_id = get_move(purchase_move_ids,line.origin)
                line.url = '%s/web#id=%s&view_type=form&model=sale.order&menu_id=%s&action=%s'%(base_url,move_id,purchase_menu_id.id,purchase_action_id.id)     


    
    url = fields.Char(
        'url',
        compute = 'get_link'
    )