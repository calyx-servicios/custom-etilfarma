from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrderBulkEdit(models.TransientModel):
    _name = 'purchase.order.bulk.edit.wizard'
    _description = 'Mass edit wizard by date'

    edition_date = fields.Date(
        string="Date for edition records",
    )

    def generate_bulk_edit_record(self):
        if self.edition_date:
            data= self.env['purchase.order'].search([])
            for rec in data:
                rec.write({'delivery_date_planned_date': self.edition_date})