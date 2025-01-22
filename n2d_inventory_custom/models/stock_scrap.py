# -*- encoding: utf-8 -*-

from odoo import models, fields, api

class StockScrap(models.Model):
    _inherit = 'stock.scrap'

    batch_id = fields.Many2one('stock.scrap.batch')