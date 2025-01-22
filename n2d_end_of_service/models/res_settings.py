# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval


class HRResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    eos_month_days = fields.Float(string="E.O.S Month Days")
    eos_debit_id = fields.Many2one('account.account', "E.O.S Debit")
    eos_credit_id = fields.Many2one('account.account', "E.O.S Credit")

    def set_values(self):
        super(HRResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('n2d_end_of_service.eos_month_days', repr(self.eos_month_days))
        params.set_param('n2d_end_of_service.eos_debit_id', self.eos_debit_id.id)
        params.set_param('n2d_end_of_service.eos_credit_id', self.eos_credit_id.id)


    @api.model
    def get_values(self):
        res = super(HRResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            eos_month_days=literal_eval(params.get_param('n2d_end_of_service.eos_month_days', 'False')),
            eos_debit_id=int(params.get_param('n2d_end_of_service.eos_debit_id', default=False)) or False,
            eos_credit_id=int(params.get_param('n2d_end_of_service.eos_credit_id', default=False)) or False

        )
        return res