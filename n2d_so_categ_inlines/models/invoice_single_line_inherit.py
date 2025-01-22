# -*- encoding: utf-8 -*-

from odoo import models, api
from num2words import num2words

class AccountInvoiceLine(models.Model):
    _inherit = 'account.move'

    def get_number_in_words(self, amount, lang):
        self.ensure_one()
        return num2words(amount, lang=lang)