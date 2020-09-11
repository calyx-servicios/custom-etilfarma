# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
"""
    The strategy that we will use will be to create new fields to show the user and 
    through them calculate the days that correspond to the number of months entered, 
    which will be dynamically dumped in the original model 'product.expiry'
"""
from odoo import api, fields, models


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    life_time_months = fields.Float(string='Product Life Time',
        help='Number of months before the goods may become dangerous and must not be consumed. It will be computed on the lot/serial number.')
    use_time_months = fields.Float(string='Product Use Time',
        help='Number of months before the goods starts deteriorating, without being dangerous yet. It will be computed on the lot/serial number.')
    removal_time_months = fields.Float(string='Product Removal Time',
        help='Number of months before the goods should be removed from the stock. It will be computed on the lot/serial number.')
    alert_time_months = fields.Float(string='Product Alert Time',
        help='Number of months before an alert should be raised on the lot/serial number.')

    @api.onchange('life_time_months')
    def _onchange_life_time_months(self):
        self.life_time = self.life_time_months * 30

    @api.onchange('use_time_months')
    def _onchange_use_time_months(self):
        self.use_time = self.use_time_months * 30

    @api.onchange('removal_time_months')
    def _onchange_removal_time_months(self):
        self.removal_time = self.removal_time_months * 30

    @api.onchange('alert_time_months')
    def _onchange_alert_time_months(self):
        self.alert_time = self.alert_time_months * 30