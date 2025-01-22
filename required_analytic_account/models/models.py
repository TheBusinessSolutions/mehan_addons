# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime




class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    default_analytic_account_id = fields.Many2one('account.analytic.account', string="Analytic account")

    @api.constrains('order_line')
    def _check_analytic_account(self):
        for rec in self:
            for line in rec.order_line:
                if not line.account_analytic_id:
                    raise ValidationError(_('Required analytic account'))



