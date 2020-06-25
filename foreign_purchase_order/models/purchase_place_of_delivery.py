from odoo import fields, models


class PlaceOfDeliver(models.Model):
    _name = "purchase.delivery"
    _rec_name = "place_of_delivery"

    # place_of_delivery = fields.One2many(
    #     comodel_name="purchase.order", inverse_name="place_of_delivery_id"
    # )
    place_of_delivery = fields.Char("Place of Delivery")
