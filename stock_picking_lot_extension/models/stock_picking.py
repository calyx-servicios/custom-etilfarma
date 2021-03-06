##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models, api, _
from odoo.exceptions import UserError

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    @api.multi
    def button_validate(self):
        order_type = self.origin
        lines_to_check = self.move_lines
        if order_type:
            if order_type[0:3] == "OCM" or order_type[0:3] == "OCE":
                record = self.env['purchase.order'].search([('name', '=', order_type)])
                for line in lines_to_check:
                    product = line.product_id
                    if product:
                        if not line.life_date:
                            raise UserError(_('You need to supply a life date for %s.') % product.display_name)
                if not record.delivery_number:
                    raise UserError(_('You need to supply a delivery number'))        
        res = super(StockPicking, self).button_validate() 
        return res             
            
