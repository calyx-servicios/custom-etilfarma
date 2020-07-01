from odoo import fields, models


class Shipment(models.Model):
    _name = "purchase.shipment"
    _rec_name = "shipment"

    shipment = fields.Char("Shipment")