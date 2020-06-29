from odoo import fields, models


class PackingList(models.Model):
    _name = "purchase.packing.list"
    _rec_name = "packing_list"

    packing_list = fields.Char("Packing List")