# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    invoice_to = fields.Many2one(
        'res.partner',
        string='Invoice to',
        index=True,
        track_visibility='onchange',
        domain=[('customer', '=', True)]
    )

    state = fields.Selection(
        selection_add=[('no_invoice', _('Without Invoice to Receive'))]
    )

    @api.multi
    def button_confirm_third_party(self):
        for order in self:
            order.write({'state': 'no_invoice'})
        return True

    @api.model
    def create(self, vals):
        new_po = super(PurchaseOrder, self).create(vals)

        purchase_orders = self.env['purchase.order'].search([
            ('invoice_to', '=', new_po.invoice_to.id),
            ('state', '=', 'no_invoice')
        ])
        purchase_orders = len(purchase_orders.filtered(lambda po: po.date_order[:4] == new_po.date_order[:4])) + 1

        new_name = '{}-{}'.format(new_po.date_order.split('-')[0], purchase_orders)
        new_po.write({'name': new_name})

        return new_po

    @api.multi
    def button_cancel_third_party(self):
        for order in self:
            order.write({'state': 'cancel'})
        return True

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        return res
