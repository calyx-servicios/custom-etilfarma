# Copyright 2020 Calyx Servicios S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api
from odoo.http import request


class PurchaseRequest(models.Model):
    _inherit = "purchase.request"

    # Create date planned field to pass as unique value and not by line.
    date_planned = fields.Datetime(string='Request Date', required=False)
    # Create all fields related to foreign_purchase_line.
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template",
        related='line_ids.product_tmpl_id',
        string='Product', readonly=True,
    )
    product_attr_id = fields.Many2one(
        comodel_name="product.attribute",
        related='line_ids.product_tmpl_id',
    )
    product_attr_value_id = fields.Many2one(
        comodel_name="product.attribute.value",
        related='line_ids.product_tmpl_id',
        string='Product', readonly=True,
    )
    purchase_order_name = fields.Char(
        string="Purchase Order",
        compute="_compute_purchase_order_name",
    )
    url = fields.Char(string="URL", compute="_compute_url")

    @api.depends('line_ids')
    def _compute_purchase_order_name(self):  
        for record in self:
            lines = record.line_ids
            record.purchase_order_name = ''
            for line in lines:
                purchases = line.purchase_lines
                for purchase in purchases:
                    record.purchase_order_name += ' ' + purchase.order_id.name

    @api.depends('url')
    def _compute_url(self):
        for record in self:
            record.url = request.env['ir.config_parameter'].get_param('web.base.url')
            record.url += '/web#id=%d&view_type=form&model=%s' % (record.id, self._name)

    @api.multi
    def send_email(self):
        template = self.env.ref('purchase_request_extension.new_purchase_request')
        self.env['mail.template'].browse(template.id).send_mail(self.id)

    @api.multi
    def button_to_approve(self):
        self.to_approve_allowed_check()
        self.send_email()
        return self.write({'state': 'to_approve'})

    @api.model
    def get_email_to(self):
        user_group = self.env.ref("purchase.group_purchase_manager")
        email_list = [
            usr.partner_id.email for usr in user_group.users if usr.partner_id.email]
        return ",".join(email_list)


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    """
        We redefine the fields 'purchased_qty' and 'product_qty' 
        to change the digits of decimal precision
    """
    purchased_qty = fields.Float(
        string='Quantity in RFQ or PO',
        digits=(12,2),
        compute="_compute_purchased_qty")
    product_qty = fields.Float(
        'Quantity', track_visibility='onchange',
        digits=(12,2))

    # Create all fields related to foreign_purchase_line.
    product_tmpl_id = fields.Many2one(comodel_name="product.template",
                                      string="Product")
    product_attr_id = fields.Many2one(
        comodel_name="product.attribute",
        string="Attribute",
        compute="_available_product_attribute",
    )
    product_attr_value_id = fields.Many2one(
        comodel_name="product.attribute.value", string="Packaging"
    )
    purchase_order_name = fields.Char(
        string="Purchase Order",
        compute="_compute_purchase_order_name",
    )
    product_id_default_code = fields.Char(string="Default Code",compute="_compute_product_id_default_code")

    @api.depends('purchase_lines')
    def _compute_purchase_order_name(self):
        for record in self:
            purchases = record.purchase_lines
            record.purchase_order_name = ''
            for purchase in purchases:
                record.purchase_order_name += ' ' + purchase.order_id.name

    # Exact copy of the method defined on foreign_purchase_lines.
    @api.depends('purchase_lines')
    def _compute_product_id_default_code(self):
        """
        Set the product_id field based in variable option selected
        in the product_attr_value_id (packaging) field
        and in the product_tmpl_id field.
        """
        for record in self:
            product_tmpl_id = record.product_tmpl_id
            product_obj = self.env["product.product"]
            domain = [("product_tmpl_id", "=", product_tmpl_id.id)]
            product_ids = product_obj.search(domain)
            for product in product_ids:
                if (
                    record.product_attr_value_id.id
                    in product.attribute_value_ids.ids
                ):
                    record.update(
                        {
                            "product_id": product.id,
                            "product_id_default_code": product.default_code,
                        }
                    )
                    break
    # Exact copy of the method defined on foreign_purchase_lines.
    @api.depends("product_tmpl_id")
    def _available_product_attribute(self):
        """
            Set the attribute with packaging option in product_attr_id field.
            This is for attribute values.
        """
        for record in self:
            product_attr_obj = self.env["product.attribute"]
            domain = [("packaging", "=", True)]
            product_attr_id = product_attr_obj.search(domain, limit=1)
            if product_attr_id:
                record.update({"product_attr_id": product_attr_id.id})
