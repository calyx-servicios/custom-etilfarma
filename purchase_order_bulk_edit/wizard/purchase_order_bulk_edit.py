from odoo import models, fields


class MassEditPlannedDeliveryDate(models.TransientModel):
    _name = 'mass.edit.planned.delivery.date'
    _description = 'Mass edit planned delivery date'

    new_date = fields.Date()

    def confirm(self):
        context = dict(self._context or {})
        active_ids = context.get('active_ids', []) or []

        purchase_orders = self.env['purchase.order'].browse(active_ids)
        purchase_orders.write({'delivery_date_planned_date':self.new_date})