# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError, UserError



class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.constrains('vat')
    def _check_unique_partner_vat(self):
        for rec in self:
            vat_duplicates = self.search([('id', '!=', rec.id), ('vat', '=', rec.vat)])
            if vat_duplicates:
                raise ValidationError('Tax ID must be unique')