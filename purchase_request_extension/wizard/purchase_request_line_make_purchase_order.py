# Copyright 2020 Calyx Servicios S.A.
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl-3.0).

from odoo import api, fields, models, _


class PurchaseRequestLineMakePurchaseOrder(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order"

    # Remove is_company from domain.
    supplier_id = fields.Many2one(
        'res.partner',
        string='Supplier',
        required=True,
        domain=[('supplier', '=', True)]
    )
    # Create other fields needed to pass values to PO.
    order_type = fields.Many2one('purchase.order.type', string="Type")
    currency_id = fields.Many2one('res.currency', string="Currency")
    invoice_to = fields.Many2one('res.partner.oct', string='Invoice to')
    send_documents_to = fields.Text(string="Send documents to",)
    marks = fields.Char(string="Marks")

    @api.model
    def _prepare_item(self, line):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)._prepare_item(line)
        res['product_tmpl_id'] = line.product_tmpl_id.id
        res['product_attr_value_id'] = line.product_attr_value_id.id
        return res

    @api.model
    def _prepare_purchase_order_line(self, po, item):
        res = super(PurchaseRequestLineMakePurchaseOrder, self)._prepare_purchase_order_line(po, item)
        res['product_tmpl_id'] = item.product_tmpl_id.id
        res['product_attr_value_id'] = item.product_attr_value_id.id
        return res

    def _write_send_document_to(self):
        info_to_write = ""
        company_id = self.env.user.company_id
        if company_id.name:
            info_to_write += _("%s\n==========\n") % company_id.name
        if company_id.street:
            info_to_write += _("Street: %s\n") % company_id.street
        if company_id.zip:
            info_to_write += _("Zip Code: %s\n") % company_id.zip
        if company_id.state_id:
            info_to_write += _("State: %s\n") % company_id.state_id.name
        if company_id.country_id:
            info_to_write += _("Country: %s\n") % company_id.country_id.name
        if company_id.main_id_number:
            info_to_write += "CUIT: {}\n".format(company_id.main_id_number)
        self.send_documents_to = info_to_write

    @api.model
    def _prepare_purchase_order(
        self, picking_type, group_id, company, origin, date_planned):
        if not self.supplier_id:
            raise UserError(
                _('Enter a supplier.'))
        supplier = self.supplier_id
        if self.invoice_to:
            self.marks = self.invoice_to.marks
        else:
            self.marks = self.env.user.company_id.marks
        self._write_send_document_to()
        data = {
            'origin': origin,
            'partner_id': self.supplier_id.id,
            'fiscal_position_id': supplier.property_account_position_id and
            supplier.property_account_position_id.id or False,
            'picking_type_id': picking_type.id,
            'company_id': company.id,
            'group_id': group_id.id,
            'date_planned': date_planned,
            'order_type': self.order_type.id,
            'currency_id': self.currency_id.id,
            'order_type_foreign': self.order_type.foreign_order,
            'invoice_to': self.invoice_to.id,
            'marks': self.marks,
            'send_documents_to': self.send_documents_to
            }
        return data

    @api.multi
    def make_purchase_order(self):
        res = []
        purchase_obj = self.env['purchase.order']
        po_line_obj = self.env['purchase.order.line']
        pr_line_obj = self.env['purchase.request.line']
        purchase = False

        for item in self.item_ids:
            line = item.line_id
            if item.product_qty <= 0.0:
                raise UserError(
                    _('Enter a positive quantity.'))
            if self.purchase_order_id:
                purchase = self.purchase_order_id
            if not purchase:
                po_data = self._prepare_purchase_order(
                    line.request_id.picking_type_id,
                    line.request_id.group_id,
                    line.company_id,
                    line.origin,
                    line.request_id.date_planned)
                purchase = purchase_obj.create(po_data)

            # Look for any other PO line in the selected PO with same
            # product and UoM to sum quantities instead of creating a new
            # po line
            domain = self._get_order_line_search_domain(purchase, item)
            available_po_lines = po_line_obj.search(domain)
            new_pr_line = True
            if available_po_lines and not item.keep_description:
                new_pr_line = False
                po_line = available_po_lines[0]
                po_line.purchase_request_lines = [(4, line.id)]
                po_line.move_dest_ids |= line.move_dest_ids
            else:
                po_line_data = self._prepare_purchase_order_line(purchase,
                                                                 item)
                if item.keep_description:
                    po_line_data['name'] = item.name
                po_line = po_line_obj.create(po_line_data)
            new_qty = pr_line_obj._calc_new_qty(
                line, po_line=po_line,
                new_pr_line=new_pr_line)
            po_line.product_qty = new_qty
            po_line._onchange_quantity()
            # The onchange quantity is altering the scheduled date of the PO
            # lines. We do not want that:
            po_line.date_planned = item.line_id.date_required
            res.append(purchase.id)

        return {
            'domain': [('id', 'in', res)],
            'name': _('RFQ'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }

    @api.onchange('supplier_id')
    def onchange_supplier_id(self):
        """
        When the partner changes, we get the order_type
        from the partner purchase_type field if this has
        a value
        """
        purchase_type = (
            self.supplier_id.purchase_type
            or self.supplier_id.commercial_partner_id.purchase_type
        )
        currency = self.supplier_id.property_purchase_currency_id
        if purchase_type:
            self.order_type = purchase_type
        if currency:
            self.currency_id = currency


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    # Create all fields related to foreign_purchase_line.
    product_tmpl_id = fields.Many2one(comodel_name="product.template",
                                      string="Product",
                                      related="line_id.product_tmpl_id")
    product_attr_id = fields.Many2one(comodel_name="product.attribute",
                                      string="Attribute",
                                      related="line_id.product_attr_id")
    product_attr_value_id = fields.Many2one(comodel_name="product.attribute.value",
                                            string="Packaging",
                                            related="line_id.product_attr_value_id")
