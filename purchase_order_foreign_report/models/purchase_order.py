# Copyright 2015 Camptocamp SA
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import models, api, _
import locale
import dateutil.parser


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.multi
    def print_purchase_foreign_report(self):
        self._check_requiered_fields()
        self._check_order_line()
        if self.state == "draft":
            self.write({"state": "sent"})
        return self.env.ref(
            "purchase_order_foreign_report.action_report_purchase_foreign"
        ).report_action(self)

    @api.multi
    def action_pfo_send(self):
        """
        This function opens a window to compose an email, with the edi
        purchase template message loaded by default
        and the purchase foreign report as attachment
        """
        self._check_requiered_fields()
        self._check_order_line()
        self.ensure_one()
        ir_model_data = self.env["ir.model.data"]
        try:
            template_id = ir_model_data.get_object_reference(
                "purchase_order_foreign_report",
                "email_template_foreign_purchase",
            )[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference(
                "mail", "email_compose_message_wizard_form"
            )[1]
        except ValueError:
            compose_form_id = False
        ctx = dict(self.env.context or {})
        ctx.update(
            {
                "default_model": "purchase.order",
                "default_res_id": self.ids[0],
                "default_use_template": bool(template_id),
                "default_template_id": template_id,
                "default_composition_mode": "comment",
                "custom_layout": "purchase.mail_template_data_notification_email_purchase_order",
                "purchase_mark_rfq_sent": True,
                "force_email": True,
            }
        )
        return {
            "name": _("Compose Email"),
            "type": "ir.actions.act_window",
            "view_type": "form",
            "view_mode": "form",
            "res_model": "mail.compose.message",
            "views": [(compose_form_id, "form")],
            "view_id": compose_form_id,
            "target": "new",
            "context": ctx,
        }

    def get_date_format_english(self):
        """
            Get the date of the order 
            and return in english format
        """
        for order in self:
            locale.setlocale(locale.LC_TIME, "en_US.UTF-8")
            date = order.date_order
            city = str(order.company_id.state_id.name)
            date = dateutil.parser.parse(date).date()
            new_date = date.strftime("%A, %B %dth, %Y")
            new_format_date = city + ", " + new_date
            return new_format_date
