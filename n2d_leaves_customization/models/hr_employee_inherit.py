# -*- coding: utf-8 -*-

from odoo import models, fields


class HREmployee(models.Model):
    _inherit = 'hr.employee'
    is_muslim = fields.Boolean('Is Muslim')
    hiring_date = fields.Date('Hiring Date')
    pass_expiration_date = fields.Date("Passport Expiration Date")
    id_expiration_date = fields.Date("ID Expiration Date")
    last_vacation_date = fields.Date("Last Vacation Date")
