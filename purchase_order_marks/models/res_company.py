from odoo import models, fields


class ResCompany(models.Model):
    _inherit = "res.company"

    marks = fields.Char(string="Marks")
