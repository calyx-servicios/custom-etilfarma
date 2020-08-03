from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner.oct'

    marks = fields.Char(string="Marks")