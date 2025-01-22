# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime,date,timedelta




class AccountBankStatement(models.Model):

    _inherit = "account.bank.statement"

    @api.model
    def create(self, vals):
        result = super(AccountBankStatement, self).create(vals)
        for record in result:
            if record.journal_type == 'bank':
                seq = self.env['ir.sequence'].next_by_code('bank.statement.sequence.custom')
            elif record.journal_type == 'cash':
                seq = self.env['ir.sequence'].next_by_code('cash.statement.sequence.custom')
            else:
                seq = False
            record.name = seq + '/' + str(record.date.year) + '/' + str(record.date.month)
        return result
