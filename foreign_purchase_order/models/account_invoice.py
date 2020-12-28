from odoo import models, api, _
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    """
        I added this functionality here to avoid to get this behavior in 
        other situations. Basicaly the Client requests to maintain 
        the same currency on the Invoice from the PO where it is
        created from.
    """

    @api.model
    def default_get(self, field_list):
        res = super(AccountInvoice, self).default_get(field_list)
        try:
            currency = (
                self.env["purchase.order"]
                .browse(self._context.get("active_ids"))
                .currency_id.id
            )
            res.update({"currency_id": currency})
        except:
            return res
        return res

    @api.onchange("document_number")
    def onchange_document_number(self):
        """
        Check the document number based in type of invoice.
        This deppends of the type of partner's afip responsability.
        If is a foreign supplier the document number don't need validation.
        """
        fa_exterior = self.env.ref("l10n_ar_account.fa_exterior").id

        if self.document_number:
            if (
                self.journal_document_type_id.document_type_id.id
                != fa_exterior
            ):
                document_number_split = (self.document_number).split(
                    "-"
                )
                if len(document_number_split) != 2:
                    raise ValidationError(
                        _(
                            "You put (%s) and Document Number must be whit a '-' in middle."
                        )
                        % (self.document_number)
                    )

                while len(document_number_split[0]) < 4:
                    document_number_split[0] = (
                        "0" + document_number_split[0]
                    )
                while len(document_number_split[1]) < 8:
                    document_number_split[1] = (
                        "0" + document_number_split[1]
                    )

                document_control = (
                    document_number_split[0]
                    + "-"
                    + document_number_split[1]
                )

            else:
                document_control = self.document_number

            self_ids = self.search(
                [
                    ("partner_id", "=", self.partner_id.id),
                    ("document_number", "=", document_control),
                ]
            )

            if len(self_ids) != 0:
                raise ValidationError(
                    _("Check Number (%s) must be unique per Partner!")
                    % (document_control)
                )
