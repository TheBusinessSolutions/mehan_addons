# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ast import literal_eval


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    petty_cash_account_id = fields.Many2one('account.account', string="Petty Cash Account")
    petty_cash_journal_id = fields.Many2one('account.journal', string="Petty Journal Id")
    employee_account_petty_cash = fields.Boolean(string='Employee Account Petty Cash')

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('n2d_petty_cash.petty_cash_account_id', repr(self.petty_cash_account_id.id))
        params.set_param('n2d_petty_cash.petty_cash_journal_id', repr(self.petty_cash_journal_id.id))
        params.set_param('n2d_petty_cash.employee_account_petty_cash', self.employee_account_petty_cash)

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            petty_cash_account_id=literal_eval(params.get_param('n2d_petty_cash.petty_cash_account_id', 'False')),
            petty_cash_journal_id=literal_eval(params.get_param('n2d_petty_cash.petty_cash_journal_id', 'False')),
            employee_account_petty_cash=params.get_param('n2d_petty_cash.employee_account_petty_cash'),
        )
        return res