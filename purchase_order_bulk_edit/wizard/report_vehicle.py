from odoo import models, fields, api, _
from odoo.exceptions import UserError


class ReportVehicle(models.TransientModel):
    _name = 'challenge.report.vehicle.wizard'
    _description = 'Report vehicle wizard'

    from_date = fields.Date(
        string="From date records",
    )

    to_date = fields.Date(
        string="To date records",
    )

    @api.constrains('from_date', 'to_date')
    def _check_field(self):
        if self.to_date == '' or self.from_date == '':
            raise UserError(_('Both fields must have value'))

    def generate_report_vehicle(self):
        domain = [
            ('create_date', '>=', self.from_date),
            ('create_date', '<=', self.to_date),
        ]
        records = self.env['challenge.register.vehicle'].search(domain)
        values = []
        for i in records:
            values.append(
                {
                    'name': i.settings_vehicle_id.name_brand,
                    'color': i.color,
                    'mileage': i.mileage,
                    'actual_price': i.actual_price
                }
            )

        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'records': values
        }
        return self.env.ref('calyx_challenge.report_vehicle_template').report_action(self, data=data)
