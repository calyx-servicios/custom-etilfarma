# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models


class PurchaseReportConfigParameter(models.Model):
    _name = "purchase.report.header.parameter"

    name = fields.Char(string="Name", required=True)
    phone = fields.Char(string="Phone", required=True)
    mail = fields.Char(string="Mail", required=True)
