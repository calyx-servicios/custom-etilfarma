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
        action_id = self.env.ref('sale.action_quotations')
        menu_id = self.env.ref('sale.menu_sale_quotations')
        move_ids = self.env['sale.order'].search([])
        for line in self:
            move_id = get_move(move_ids,line.origin)
            line.url = '%s/web#id=%s&view_type=form&model=sale.order&menu_id=%s&action=%s'%(base_url,move_id,menu_id.id,action_id.id)

    
    url = fields.Char(
        'url',
        compute = 'get_link'
    )