from odoo import fields, models, api, _

class StockPicking(models.Model):
    _inherit = "stock.move"

    gross_weight_pallet = fields.Float(_('Gross Weight Pallet'),compute="_compute_gross_weight_pallet")

    packages_qty = fields.Integer(
        sting="Packages Quantity",
        compute="_compute_packages_qty"
    )

    @api.depends('product_id','packages_qty')
    def _compute_packages_qty(self):
        for rec in self:
            rec.packages_qty = rec.quantity_done / rec.product_id.quantity_per_package
            rec.net_weight = rec.packages_qty * rec.product_id.weight
            rec.gross_weight =  rec.packages_qty * rec.product_id.gross_weight

    @api.depends('gross_weight_pallet')
    def _compute_gross_weight_pallet(self):
        for rec in self:
            rec.gross_weight_pallet = rec.gross_weight + rec.pallet_type.weight

