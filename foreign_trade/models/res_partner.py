# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_type = fields.Many2one(
        comodel_name='sale.order.type', string='Sale Order Type')

    @api.multi
    def _get_partner_banks(self):
        bank_data = self.env['res.partner.bank'].search([('partner_id', '=', self.id)])
        return bank_data

    default_bank = fields.Many2one(
        'res.partner.bank', 
        string='Default Bank', 
    )




