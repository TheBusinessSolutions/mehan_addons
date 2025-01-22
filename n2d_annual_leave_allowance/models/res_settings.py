# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval


class HRResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    month_days = fields.Float(string="No. of Month Days")
    leave_debit_id = fields.Many2one('account.account', "Leave Debit")
    leave_credit_id = fields.Many2one('account.account', "Leave Credit")

    def set_values(self):
        super(HRResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('n2d_annual_leave_allowance.month_days', repr(self.month_days))
        params.set_param('n2d_annual_leave_allowance.leave_debit_id', self.leave_debit_id.id)
        params.set_param('n2d_annual_leave_allowance.leave_credit_id', self.leave_credit_id.id)


    @api.model
    def get_values(self):
        res = super(HRResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            month_days=literal_eval(params.get_param('n2d_annual_leave_allowance.month_days', 'False')),
            leave_debit_id=int(params.get_param('n2d_annual_leave_allowance.leave_debit_id',  default=False)) or False,
            leave_credit_id=int(params.get_param('n2d_annual_leave_allowance.leave_credit_id',  default=False)) or False
        )
        return res