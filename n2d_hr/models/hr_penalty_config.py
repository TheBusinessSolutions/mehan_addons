# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HRPenaltyConfig(models.Model):
    _name = 'hr.penalty.confg'

    name = fields.Char("Penalty Name")
    penalty_amount = fields.Float("Amount")


    @api.constrains('penalty_amount')
    def validate_amount(self):
        for rec in self:
            if rec.penalty_amount <= 0:
                raise ValidationError("Amount Must Be Greater Than Zero!!")
