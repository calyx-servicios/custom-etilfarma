from odoo import fields, models, api

class PalletType(models.Model):
    _name = "pallet.type"

    name = fields.Char(string="Pallet Type")
    weight = fields.Float(string="Weight")

class StockPicking(models.Model):
    _inherit = "stock.picking"

    order_type_foreign = fields.Boolean(
        string = "Is Foreign Trade Order",
        related = "sale_id.order_type_foreign",
    )
    incoterm = fields.Char(
        string = "Incoterm",
        related = "sale_id.incoterm_id.code"    
    )
    shipping = fields.Char(
        string = "Shipping",
        related = "sale_id.shipment_id.display_name"
    )
    carrier = fields.Text(
        string = "Carrier",
        related = "sale_id.carriers"
    )
    place_of_delivery = fields.Char(
        string="Place of Delivery",
        related="sale_id.partner_id.contact_address"
    )
    delivery_term = fields.Char(
        string="Delivery Term",
        related="sale_id.place_of_delivery_id.place_of_delivery"
    )
    remarks_packing_list = fields.Text(
        string='Remarks on Packing List'
    )
    packing_list_number = fields.Char(
        string="Packing List Number"
    )
    container = fields.Char(
        string="Container"
    )

    seq = fields.Char(
        string="Sequence",
        required=True,
    )

    @api.model
    def create(self, vals):
        if not vals.get('seq'):
            vals['seq'] = self.env['ir.sequence'].next_by_code(
                'stock.picking')
        return super(StockPicking, self).create(vals)


class StockMove(models.Model):
    _inherit = "stock.move"

    packaging = fields.Char(
        string="Packaging",
        related="sale_line_id.product_attr_value_id.name"
    )    
    stock_move_line_seq = fields.Integer(
        string="Item",
        related="sale_line_id.order_line_seq"
    )
    product_nmc_code = fields.Char(
        string="HS Code",
        related="product_id.product_nmc"
    )
    country = fields.Char(
        string="Origin",
        related="product_id.country_id.name"
    )
    net_weight = fields.Float(
        string="Net Weight",
        compute="_compute_net_weight"
    )
    gross_weight = fields.Float(
        string="Gross Weight",
        compute="_compute_gross_weigth"
    )
    packages_qty = fields.Integer(
        sting="Packages Quantity"
    )
    pallet_qty = fields.Integer(
        sting="Pallet Quantity"
    )
    pallet_type = fields.Many2one(
        sring="Pallet Type",
        comodel_name="pallet.type"
    )
     
    @api.depends('net_weight','pallet_qty','pallet_type')
    def _compute_gross_weigth(self):
        for rec in self:
            rec.gross_weight = rec.net_weight + rec.pallet_qty * rec.pallet_type.weight

    @api.depends('product_qty','product_id')
    def _compute_net_weight(self):
        for rec in self:
            rec.net_weight = rec.product_qty * rec.product_id.weight
