# -*-coding: utf-8 -*-

from odoo import models, fields, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    analytic_account = fields.Many2one('account.analytic.account', string="Analytic Account", required=True)
