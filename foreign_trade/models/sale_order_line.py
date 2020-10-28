from odoo import fields, models, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

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

    @api.onchange("product_attr_value_id")
    def _onchange_product_attr_value_id(self):
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
                    record.update({"product_id": product.id})
                    break

    @api.depends('sequence', 'order_id')
    def _compute_get_order_line_seq(self):
        for order in self.mapped('order_id'):
            order_line_seq = 1
            for line in order.order_line:
                line.order_line_seq = order_line_seq
                order_line_seq += 1

    @api.onchange("product_tmpl_id")
    def _onchange_product_tmpl_id(self):
        """
            Check if the product has variants if doesn't 
            set the normal product_id
            Add a dinamic domain in the product_attr_value_id based in the
            product template.
            This only show attribute values set in the product.
        """
        for record in self:
            values_ids = []
            product_tmpl_id = record.product_tmpl_id.id
            attri_value_line_obj = self.env["product.attribute.line"]
            search_domain = [("product_tmpl_id", "=", product_tmpl_id)]
            attr_value_ids = attri_value_line_obj.search(
                search_domain, limit=1
            )
            if attr_value_ids:
                for value in attr_value_ids.value_ids:
                    values_ids.append(value.id)
            else:
                product_obj = self.env["product.product"]
                produc_id = product_obj.search(search_domain, limit=1)
                if produc_id:
                    record.product_id = produc_id.id
            if product_tmpl_id:
                if not self.country_id:
                    raise UserError(_("You must define the 'Origin' field in the product template model."))

            domain = [("id", "in", values_ids)]

        return {"domain": {"product_attr_value_id": domain}}
    
    order_line_seq = fields.Integer(
        compute='_compute_get_order_line_seq',
        store=True,
    )
    product_tmpl_id = fields.Many2one(
        comodel_name="product.template", string="Product"
    )
    product_attr_id = fields.Many2one(
        comodel_name="product.attribute",
        string="Attribute",
        compute="_available_product_attribute",
    )
    product_attr_value_id = fields.Many2one(
        comodel_name="product.attribute.value", string="Packaging"
    )

    product_nmc = fields.Char(string="HS Code", related="product_id.product_nmc")
    country_id = fields.Char(string="Origin", required=True, related="product_tmpl_id.country_id.name")
    observations = fields.Char(string="Observation")
    loot_name = fields.Char(string="Loot Name")
    life_date = fields.Datetime(string="Life Date")
    product_qty = fields.Float(digits=(12,2))
    qty_received = fields.Float(digits=(12,2))
    qty_invoiced = fields.Float(digits=(12,2))
