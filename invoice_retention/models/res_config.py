# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResCompany(models.Model):
    _inherit = "res.company"

    retention_product_id = fields.Many2one('product.product', string='Retention Product')
    retention_percentage = fields.Float(string='Retention Percentage')


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    retention_product_id = fields.Many2one('product.product', string='retention Product')
    retention_percentage = fields.Float(string='Retention Percentage')



