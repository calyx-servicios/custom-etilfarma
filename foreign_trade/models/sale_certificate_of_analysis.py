from odoo import fields, models, _
from odoo.exceptions import Warning


class SaleCertificateOfAnalysis(models.Model):
    _name = "sale.certificate.analysis"
    _rec_name = "certificate_of_analysis"
    _order = "sequence"

    certificate_of_analysis = fields.Char("Certificate of Analysis")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        sale_obj = self.env["sale.order"]
        rule_ranges = sale_obj.search([("certificate_of_analysis", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more sale, "
                    "try to archive it."
                )
            )
        return super(SaleCertificateOfAnalysis, self).unlink()
