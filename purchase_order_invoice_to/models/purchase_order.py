# -*- coding: utf-8 -*-
# Copyright 2018 Raphael Reverdy https://akretion.com
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime, timedelta
import dateutil.parser
from odoo import api, fields, models, _
from odoo.exceptions import Warning


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.depends("date_order")
    def _compute_date_order_stats(self):
        for po in self:
            po.date_order_stats = datetime.strptime(
                    po.date_order, "%Y-%m-%d %H:%M:%S"
                ).date()

    def _default_order_types(self):
        if self._context.get("ima"):
            return self.env.ref("purchase_order_invoice_to.po_type_third_party").id
        else:
            return self.env.ref("purchase_order_types.po_type_regular").id

    @api.multi
    def _domain_order_type(self):
        oct_order = self.env.ref("purchase_order_invoice_to.po_type_third_party").id
        if self._context.get("ima"):
            return [("id", "=", oct_order)]
        else:
            return [("id", "!=", oct_order)]

    invoice_to = fields.Many2one(
        'res.partner.oct',
        string='Invoice to',
        index=True,
        track_visibility='onchange'
    )

    state = fields.Selection(
        selection_add=[('no_invoice', _('Without Invoice to Receive'))]
    )

    third_party_number = fields.Integer(
        help='Enumeration for the Third Party Order by Client and by Year',
        )

    send_document_to_invoice_to = fields.Boolean(
        string='Send Documents to Client'
    )

    use_other_invoice_to_address = fields.Many2one(
        string="Use another Client Address?",
        comodel_name="res.partner.oct.addresses",
    )

    order_type = fields.Many2one(
        domain=_domain_order_type, 
        default=_default_order_types
    )

    product_qty = fields.Float("Quantity", related="order_line.product_qty" )
    invoice_due_date = fields.Date("Invoice Due Date")
    date_order_stats = fields.Date("Order Date", compute="_compute_date_order_stats")

    def order_name_copy(self):
        split_order = self.name.split("-")
        not_unique = True
        new_order = ""
        if len(split_order) == 1:
            self.not_unique = False
        while not_unique:
            if len(split_order) == 2:
                new_order= self.name + "-A"
            elif len(split_order) == 3:
                new_order = split_order[0] + "-" + split_order[1] + "-" + chr(ord(split_order[2])+1)
            check_order = self.env["purchase.order"].search([('name', '=', new_order)])
            if check_order:
                split_order = new_order.split("-")
            else:
                not_unique = False
        self.order_name = new_order

    order_name = fields.Char(compute="order_name_copy")
    has_copy = fields.Boolean(default=False)
    original = fields.Boolean(default=False)
    copied = fields.Boolean(default=False)

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
        split_order_name= self.name.split("-")
        if len(split_order_name) >= 2:
            order_name = "{}-{}".format(split_order_name[0],split_order_name[1])
            original_order = self.env["purchase.order"].search([
                ("name", "=", order_name)
            ], limit=1)
            for line in self.order_line:
                if line.confirm_product:
                    for original_line in original_order.order_line:
                        if original_line.product_id_origin == line.product_id_origin:
                            original_line.confirm_product = True
            self._check_requiered_fields()
            self._check_order_line()
            self.write({'state': 'no_invoice'})
            return True

    @api.multi
    def button_create_order(self):
        self.has_copy = True
        self.original = True
        vals = {
            'has_copy': False,
            'original': False,
            'copied': True,
        }
        new_record = self.copy(default=vals)
        line_cont = 0
        split_order_name= self.name.split("-")
        if len(split_order_name) >= 2:
            order_name = "{}-{}".format(split_order_name[0],split_order_name[1])
            original_order = self.env["purchase.order"].search([
                ("name", "like", order_name),("original", "=", True)
            ], limit=1)
            duplicated_order = self.env["purchase.order"].search([
                ("name", "like", order_name),("copied", "=", True)
            ], limit=1)
            for line in original_order.order_line:
                if not line.confirm_product and line.purchase_order_created and line.tracked_line:
                    line.write({'tracked_line': False})
                    line.write({'purchase_order_created': False})
                    if original_order.name != order_name:
                        original_order.order_line = [(2,line.id ,0)]  
            original_order.write({'original': False})  
            for line in duplicated_order.order_line:
                if not line.confirm_product and not line.purchase_order_created and line.tracked_line:
                    line.write({'tracked_line': False})
                if not line.confirm_product and line.purchase_order_created and line.tracked_line:
                    line.write({'purchase_order_created': False})
                if line.confirm_product and not line.purchase_order_created and line.tracked_line:
                    line.write({'tracked_line': False})
                if not line.tracked_line:
                    duplicated_order.order_line = [(2,line.id ,0)]
            duplicated_order.write({'copied': False})
            return {
                    'type': 'ir.actions.act_window',
                    'res_model': 'purchase.order',
                    'res_id': new_record.id,
                    'view_mode': 'form',
                    "context":{'search_default_todo':1, 'show_purchase': True, 'show_invoice_to': 1,'ima': True},
                    }

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
            elif not self.has_copy:
                new_po.third_party_number = last_purchase_order_oct_num.third_party_number + 1

            new_name = '{}-{}'.format(new_po.date_order.split('-')[0], new_po.third_party_number)
            if not self.has_copy:
                new_po.write({'name': new_name})
            else:
                new_po.write({'name': self.order_name})

        return new_po

    @api.multi
    def button_approve(self, force=False):
        """
        when the Order Type is OCT the confirm action will not create
        a picking order.
        """
        self.write(
            {
                "state": "purchase",
                "date_approve": fields.Date.context_today(self),
            }
        )
        if (
            self.order_type.id
            != self.env.ref(
                "purchase_order_invoice_to.po_type_third_party"
            ).id
        ):
            self._create_picking()
        self.filtered(lambda p: p.company_id.po_lock == "lock").write(
            {"state": "done"}
        )
        return {}


    @api.multi
    def button_cancel_third_party(self):
        for order in self:
            order.write({'state': 'cancel'})
        return True

    @api.multi
    @api.onchange('term_payments','documents_FC_date')
    def _onchange_term_patments(self):
        for rec in self:
            if rec.term_payments and rec.documents_FC_date:
                try:
                    term = int(rec.term_payments.name.split(" ")[0])
                    date = dateutil.parser.parse(rec.documents_FC_date).date()
                    new_date = date + timedelta(days=term)
                    rec.invoice_due_date = new_date
                except:
                    rec.invoice_due_date = rec.documents_FC_date

    @api.multi
    @api.onchange('partner_id')
    def onchange_partner_id(self):
        res = super(PurchaseOrder, self).onchange_partner_id()
        order_oct = self.env.ref("purchase_order_invoice_to.po_type_third_party").id
        if self._context.get("ima"):
            self.order_type = order_oct
        return res

    @api.multi
    @api.onchange('order_line')
    def onchange_order_lines(self):
        if len(self.name.split("-")) == 2 or self.name == "New": 
            req = 0
            for line in self.order_line:
                line.product_id_origin = req
                req += 1

    @api.onchange('invoice_to')
    def _invoice_to_for_opt_address(self):
        res = {
            'domain': {
                'use_other_invoice_to_address': [('id', 'in', self.invoice_to.optional_address.ids)],
            }
        }
        return res

    @api.onchange("send_document_to_invoice_to", "invoice_to", "use_other_invoice_to_address")
    def _onchange_send_document_to_invoice_to(self):
        """
            We check if send_document_to_invoice_to boolean field is selected.
            If it is, send_document_to takes the invoice_to partner values.
            If it is not, send_document_to is written with the company values.
            - We also rewrite the field if the invoice_to partner is changed.
        """
        for record in self:
            if record.send_document_to_invoice_to:
                if record.invoice_to and record.use_other_invoice_to_address:
                    self._write_send_document_to(record.use_other_invoice_to_address)
                elif record.invoice_to:
                    self._write_send_document_to(record.invoice_to)
                else:
                    raise Warning(_('Please Select Client to Invoice, and check the option again.'))
            else:
                self._write_send_document_to(self.company_id)

    def _write_send_document_to(self, record):
        info_to_write = ""

        if record.name:
            info_to_write += _("%s\n==========\n") % record.name
        if record.street:
            info_to_write += _("Street: %s\n") % record.street
        if record.zip:
            info_to_write += _("Zip Code: %s\n") % record.zip
        if record.state_id:
            info_to_write += _("State: %s\n") % record.state_id.name
        if record.country_id:
            info_to_write += _("Country: %s\n") % record.country_id.name
        if record.main_id_number:
            info_to_write += "CUIT: {}\n".format(record.main_id_number)

        self.send_documents_to = info_to_write
