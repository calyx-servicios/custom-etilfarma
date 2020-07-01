# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    special_indications = fields.Text(string='Special Indications Default')

    @api.model
    def get_values(self):
        res = super().get_values()
        icpsudo = self.env['ir.config_parameter'].sudo()  # icpsudo -> Ir.Config_Parameter access with sudo()
        indications = icpsudo.get_param('foreign_purchase_order.special_indications')
        res.update(
            special_indications=indications
        )
        return res

    @api.multi
    def set_values(self):
        res = super().set_values()
        self.env['ir.config_parameter'].set_param('foreign_purchase_order.special_indications', self.special_indications)
        return res
