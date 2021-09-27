# -*- coding: utf-8 -*-

from odoo import api, models, _
from odoo.exceptions import Warning


class PurchaseOrderForeignReport(models.AbstractModel):
    _name = "report.purchase_order_foreign_report.po_foreign_r"

    @api.model
    def get_report_values(self, docids, data=None):
        docs = self.env["purchase.order"].browse(docids)
        header_parameters_obj = self.env.ref(
            "purchase_order_foreign_report.report_header_parameters"
        )

        if not header_parameters_obj:
            raise Warning(
                _(
                    "You try to print this report"
                    "without header parameters, please try adding them first"
                )
            )

        header_name = str(header_parameters_obj.name)
        header_mail = str(header_parameters_obj.mail)
        header_phone = str(header_parameters_obj.phone)
        countries_translations = self.env['ir.translation'].search([('name','=','res.country,name')])
        country_dict = {name.value : name.src for name in countries_translations}
        
        return {
            "doc_ids": docids,
            "doc_model": self.env["purchase.order"],
            "data": data,
            "docs": docs,
            "header_name": header_name,
            "header_mail": header_mail,
            "header_phone": header_phone,
            "country_dict": country_dict,
        }

