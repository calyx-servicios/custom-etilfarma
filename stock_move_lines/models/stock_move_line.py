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
        purchase_action_id = self.env.ref('purchase.purchase_form_action')
        purchase_menu_id = self.env.ref('purchase.menu_purchase_form_action')
        purchase_move_ids = self.env['purchase.order'].search([])
        # If move is sale
        sales_action_id = self.env.ref('sale.action_quotations')
        sales_menu_id = self.env.ref('sale.menu_sale_quotations')
        sales_move_ids = self.env['sale.order'].search([])
        #Get Sale and Purchase sequence prefix
        sales_prefix = self.env['ir.sequence'].search([('sale_seq','=',True)])
        purchase_prefix = self.env['ir.sequence'].search([('purchase_seq','=',True)])
        for line in self:
            if "SO" in line.origin:
                move_id = get_move(sales_move_ids,line.origin)
                line.url = '%s/web#id=%s&view_type=form&model=sale.order&menu_id=%s&action=%s'%(base_url,move_id,sales_menu_id.id,sales_action_id.id)
                #line.url = 
            elif "OC" or "p" in line.origin:
                move_id = get_move(purchase_move_ids,line.origin)
                #line.url = '%s/web#id=%s&view_type=form&model=purchase.order&menu_id=%s&action=%s'%(base_url,move_id,purchase_menu_id.id,purchase_action_id.id)     


    def get_url(self):
        base_url = base_url = http.request.env['ir.config_parameter'].get_param('web.base.url')
        sales_action_id = self.env.ref('sale.action_quotations')
        sales_move_id = self.env['sale.order'].search([('name','=',self.origin)])
        sales_menu_id = self.env.ref('sale.menu_sale_quotations')
        purchase_action_id = self.env.ref('purchase.purchase_form_action')
        purchase_menu_id = self.env.ref('purchase.menu_purchase_form_action')
        purchase_move_id = self.env['purchase.order'].search([('name','=',self.origin)])
        if "SO" in self.origin:
            #move_id = get_move(sales_move_ids,self.origin)
            return ('%s/web#id=%s&view_type=form&model=sale.order&menu_id=%s&action=%s'%(base_url,sales_move_id,sales_menu_id.id,sales_action_id.id))
            #self.url = 
        elif "OC" or "p" in self.origin:
            #move_id = get_move(purchase_move_ids,self.origin)
            return ('%s/web#id=%s&view_type=form&model=purchase.order&menu_id=%s&action=%s'%(base_url,purchase_move_id,purchase_menu_id.id,purchase_action_id.id))

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

    url = fields.Char(
        'url',
        compute = 'get_link'
    )