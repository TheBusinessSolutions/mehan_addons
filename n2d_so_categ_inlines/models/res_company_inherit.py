# -*- encoding: utf-8 -*-

from odoo import models, fields, api

class StockPicking(models.Model):
    _inherit = 'res.company'

    tax_no = fields.Char("Tax No")
    tax_file_no = fields.Char("Tax File No")

