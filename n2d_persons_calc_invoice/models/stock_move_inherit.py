# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class StockMove(models.Model):
    _inherit = 'stock.move'

    dish_id = fields.Many2one('party.dishes')