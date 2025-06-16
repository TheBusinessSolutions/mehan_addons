#-*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountBankStatementLine(models.Model):
    _inherit = "account.bank.statement.line"

    partner_vat = fields.Char(related='partner_id.vat')