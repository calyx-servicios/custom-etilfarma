from odoo import fields, models, _
from odoo.exceptions import Warning


class PurchaseImportLicense(models.Model):
    _name = "purchase.import.license"
    _rec_name = "import_license"
    _order = "sequence"

    import_license = fields.Char("Import license")
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def unlink(self):
        purchase_obj = self.env["purchase.order"]
        rule_ranges = purchase_obj.search([("import_license", "=", self.id)])
        if rule_ranges:
            raise Warning(
                _(
                    "You are trying to delete a record "
                    "that is still referenced in one o more purchase, "
                    "try to archive it."
                )
            )
        return super(PurchaseImportLicense, self).unlink()
