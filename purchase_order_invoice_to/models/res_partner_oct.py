# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class Partner(models.Model):
    _description = 'OCT Contact'
    _name = "res.partner.oct"
    _order = "name"

    @api.model
    def _lang_get(self):
        return self.env['res.lang'].get_installed()

    image = fields.Binary("Image", attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px", )

    name = fields.Char(index=True)
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='invoice',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")
    street = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    city = fields.Char()
    zip = fields.Char()
    street2 = fields.Char()

    afip_responsability_type_id = fields.Many2one(
        'afip.responsability.type',
        'AFIP Responsability',
        auto_join=True,
        index=True,
    )
    main_id_number = fields.Char(
        string='Main Identification Number',
    )
    main_id_category_id = fields.Many2one(
        'res.partner.id_category',
        string="Main Identification Category"
    )

    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    website = fields.Char(help="Website of Partner or Company")
    title = fields.Many2one('res.partner.title')
    lang = fields.Selection(_lang_get, string='Language', default=lambda self: self.env.lang,
                            help="If the selected language is loaded in the system, all documents related to "
                                 "this contact will be printed in this language. If not, it will be English.")

    comment = fields.Text(string='Notes')
    active = fields.Boolean(default=True)
    ref = fields.Char(string='Internal Reference', index=True)

    invoice_to = fields.One2many(
        comodel_name="purchase.order",
        inverse_name="invoice_to"
    )

    optional_address = fields.One2many(
        comodel_name="res.partner.oct.addresses",
        inverse_name="partner_oct"
    )


class PartnerOptionalAddresses(models.Model):
    _description = 'OCT Contact Optional Addresses'
    _name = "res.partner.oct.addresses"

    name = fields.Char()
    type = fields.Selection(
        [('contact', 'Contact'),
         ('invoice', 'Invoice address'),
         ('delivery', 'Shipping address'),
         ('other', 'Other address'),
         ("private", "Private Address"),
         ], string='Address Type',
        default='invoice',
        help="Used to select automatically the right address according to the context in sales and purchases documents.")
    street = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict')
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    city = fields.Char()
    zip = fields.Char()
    street2 = fields.Char()

    phone = fields.Char()
    mobile = fields.Char()
    email = fields.Char()
    comment = fields.Text(string='Notes')

    partner_oct = fields.Many2one(
        comodel_name="res.partner.oct",
    )

    main_id_number = fields.Char(related='partner_oct.main_id_number')