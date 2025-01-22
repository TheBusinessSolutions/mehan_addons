# -*- encoding: utf-8 -*-

from odoo import models, fields

class Supplierinfo(models.Model):
    _inherit = 'product.supplierinfo'

    categ_id = fields.Many2one("product.category", string="Category")