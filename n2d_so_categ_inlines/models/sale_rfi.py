# -*- encoding: utf-8 -*-

from odoo import fields, models

class SaleRFI(models.Model):
    _name = 'sale.rfi'

    name = fields.Char("Name", required=True)