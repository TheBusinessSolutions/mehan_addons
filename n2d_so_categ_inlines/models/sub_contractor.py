# -*- encoding: utf-8 -*-

from odoo import fields, models


class SubContractor(models.Model):
    _name = 'sub.contractor'

    name = fields.Char("Name", required=True)
