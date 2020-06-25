# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from odoo import api, fields, models, _
from odoo.exceptions import Warning


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

    third_party_number = fields.Integer(
        help='Enumeration for the Third Party Order by Client and by Year',
        )

    @staticmethod
    def _get_date_range(date_order_str):
        """
        Receive a date string, returning two strings of
        the first and last day of the year.

        :param date_order_str:
        :return: string
        """
        date_order = fields.Datetime.from_string(date_order_str)
        date_from = datetime(date_order.year, 1, 1).strftime("%Y-%m-%d %H:%M:%S")
        date_to = datetime(date_order.year, 12, 31, 23, 59, 59).strftime("%Y-%m-%d %H:%M:%S")
        return date_from, date_to

    def _get_last_purchase_order_oct_num(self, invoice_to_partner_id, date_from, date_to):
        """
        Returns the last OCT Purchase Order of the Client, between the
        Dates received with OCT number assigned.

        :param invoice_to_partner_id: integer
        :param date_from: string
        :param date_to: string
        :return: purchase.order object
        """
        last_purchase_order_oct_num = self.env['purchase.order'].search([
            ('invoice_to', '=', invoice_to_partner_id),
            ('state', 'in', ['draft', 'no_invoice', 'cancel']),
            ('order_type', '=', self.env.ref('purchase_order_invoice_to.po_type_third_party').id),
            ('date_order', '>=', date_from),
            ('date_order', '<=', date_to),
            ('third_party_number', '!=', False)
        ], order='third_party_number desc', limit=1)
        return last_purchase_order_oct_num

    @api.multi
    def button_confirm_third_party(self):
        for order in self:
            order.write({'state': 'no_invoice'})
        return True

    @api.model
    def create(self, vals):
        """
        Assign the Name of the PO with the year and corresponding number
        if the type is OCT.
        """
        new_po = super(PurchaseOrder, self).create(vals)

        if new_po.order_type.id == self.env.ref('purchase_order_invoice_to.po_type_third_party').id:

            date_from, date_to = self._get_date_range(new_po.date_order)
            last_purchase_order_oct_num = self._get_last_purchase_order_oct_num(
                new_po.invoice_to.id,
                date_from,
                date_to)

            if not last_purchase_order_oct_num:
                new_po.third_party_number = 1
            else:
                new_po.third_party_number = last_purchase_order_oct_num.third_party_number + 1

            new_name = '{}-{}'.format(new_po.date_order.split('-')[0], new_po.third_party_number)
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
