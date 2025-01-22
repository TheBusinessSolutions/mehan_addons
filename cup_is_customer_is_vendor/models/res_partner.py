# -*- coding: utf-8 -*-

from odoo import models, fields, api

class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Is a Customer',
                                help="Check this box if this contact is a customer. It can be selected in sales orders.")
    is_supplier = fields.Boolean(string='Is a Vendor',
                                help="Check this box if this contact is a vendor. It can be selected in purchase orders.")
    