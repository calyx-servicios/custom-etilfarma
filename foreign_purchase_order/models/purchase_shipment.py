from odoo import fields, models


class PlaceOfDeliver(models.Model):
    _name = "purchase.shipment"
    _rec_name = "shipment"

    shipment = fields.Char("Shipment")