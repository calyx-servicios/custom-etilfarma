# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from datetime import datetime

from odoo import fields, models, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    order_type_foreign = fields.Boolean(string="Foreign Order", default=False)

    purchase_sample = fields.Boolean(string="Sample?", default=False)

    customer_purchase_order = fields.Char(string="Customer Purchase Order")

    place_of_delivery_id = fields.Many2one(
        comodel_name="purchase.delivery",
        string="Place of Delivery",
        ondelete="restrict",
    )

    packaging_id = fields.Many2one(
        comodel_name="purchase.packaging",
        string="Packaging",
        ondelete="restrict",
    )

    delivery_date_week = fields.Char(
        string="Delivery Date (Week)",
        compute="_compute_delivery_date_week",
        store=True,
    )

    send_documents_to = fields.Text(string="Send documents to",)

    shipment_id = fields.Many2one(
        comodel_name="purchase.shipment",
        string="Shipment",
        ondelete="restrict",
    )
    import_license_id = fields.Many2one(
        comodel_name="purchase.import.license",
        string="Import License",
        ondelete="restrict",
    )
    certificate_of_analysis_id = fields.Many2one(
        comodel_name="purchase.certificate.analysis",
        string="Certificate of Analysis",
        ondelete="restrict",
    )
    packing_list_id = fields.Many2one(
        comodel_name="purchase.packing.list",
        string="Packing List",
        ondelete="restrict",
    )
    term_payments = fields.Many2one(
        # The base purchase.order model already has a m2o rel
        # with account.payment.term
        # but this correspond to a custom request by the client.
        comodel_name="account.payment.term",
        string="Terms of Payment",
    )

    extra_notes = fields.Text(string="Extra", size=150)

    import_license_approval_date = fields.Date(
        string="Import License Approval Date"
    )
    import_license_issue_date = fields.Date(string="Import License Issue Date")
    import_license_number = fields.Char(string="Import License Number")
    bill_landing_number = fields.Char(string="Bill Landing Number")
    bill_landing_issue_date = fields.Date(string="Bill Landing Issue Date")
    bill_landing_reception_date = fields.Date(
        string="Bill Landing Reception Date"
    )
    bill_landing_description = fields.Char(string="Bill Landing Description")
    delivery_number = fields.Char(string="Import Delivery Number")
    delivery_date = fields.Date(string="Import Delivery Date")

    @api.onchange("order_type")
    def _onchange_order_type(self):
        """
            When the order type changes, check if that order is a foreign order
            if it is, then set like True the variable order_type_foreign 
            to show some fields in the purchase view.
        """
        for record in self:
            if record.order_type:
                if record.order_type.foreign_order:
                    record.order_type_foreign = True
                else:
                    record.customer_purchase_order = ""
                    record.order_type_foreign = False

            else:
                record.customer_purchase_order = ""
                record.order_type_foreign = False

    @api.depends("date_planned")
    def _compute_delivery_date_week(self):
        """
        We take the date_planned assigned by the user to
        format it into the regular format.
        Then we concatenate a string with that formmated
        date plus the week number
        """
        for po in self:
            if po.date_planned:
                date_fmt = "/".join(
                    reversed(po.date_planned.split(" ")[0].split("-"))
                )
                po.delivery_date_week = "{} - W{}".format(
                    date_fmt,
                    datetime.strptime(
                        po.date_planned, "%Y-%m-%d %H:%M:%S"
                    ).isocalendar()[1],
                )

    @api.onchange("purchase_sample")
    def _onchange_purchase_sample(self):
        """
        When the purchase_sample is True, we get the purchase sample type
        and set in the purchase_type field,
        however if the purchase_sample is false, we get the purchase type
        in the partner and set in purchase_type field.
        """
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        ocl = self.env.ref("purchase_order_types.po_type_regular")
        purchase_type = (
            self.partner_id.purchase_type
            or self.partner_id.commercial_partner_id.purchase_type
        )
        for record in self:
            if ocm:
                if record.purchase_sample:
                    record.order_type = ocm.id
                    if ocm.foreign_order:
                        record.order_type_foreign = True
                else:
                    if purchase_type:
                        record.order_type = purchase_type
                    else:
                        record.order_type = ocl.id

    @api.multi
    @api.onchange("partner_id")
    def onchange_partner_id(self):
        """
        When the partner change and if purchase_sample it is true
        then the order_type keeps in ocm
        """
        super().onchange_partner_id()
        ocm = self.env.ref("purchase_order_types.po_type_sample")
        if self.purchase_sample:
            self.order_type = ocm.id

    def _get_invoiced(self):
        """
         Inherit to force sample POs to be in 'Nothing to Bill' state
        """
        super(PurchaseOrder, self)._get_invoiced()
        for order in self.filtered(
            lambda po: po.purchase_sample and po.invoice_status == "to invoice"
        ):
            order.invoice_status = "no"

    @api.multi
    def _get_default_special_indications(self):
        """
         Set the Special Indications based on the value of the
         field in Purchase settings
        """
        icpsudo = self.env[
            "ir.config_parameter"
        ].sudo()  # icpsudo -> Ir.Config_Parameter access with sudo()
        indications = icpsudo.get_param(
            "foreign_purchase_order.special_indications"
        )
        return indications

    special_indications = fields.Text(
        string="Special Indications", default=_get_default_special_indications
    )

