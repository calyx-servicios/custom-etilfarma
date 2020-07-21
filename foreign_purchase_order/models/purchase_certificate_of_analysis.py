from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseCertificateOfAnalysis(models.Model):
    _name = "purchase.certificate.analysis"
    _rec_name = "certificate_of_analysis"
    _order = "sequence"

    certificate_of_analysis = fields.Char("Certificate of Analysis / COA")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("certificate_of_analysis", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseCertificateOfAnalysis, self).unlink()
