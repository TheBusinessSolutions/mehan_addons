# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HRBonusConfig(models.Model):
    _name = 'hr.bonus.confg'

    name = fields.Char("Bonus Name")
    bonus_amount = fields.Float("Amount")


    @api.constrains('bonus_amount')
    def validate_amount(self):
        for rec in self:
            if rec.bonus_amount <= 0:
                raise ValidationError("Amount Must Be Greater Than Zero!!")
