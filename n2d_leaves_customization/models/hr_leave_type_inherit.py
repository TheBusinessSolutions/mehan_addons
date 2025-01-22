# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHolidayStatus(models.Model):
    _inherit = 'hr.leave.type'

    is_unpaid = fields.Boolean("Unpaid")
    allow_days_off = fields.Boolean("Allow Days Off")
    leave_type = fields.Selection(
        [('haj', 'Haj'), ('dead', 'Dead'), ('husband_dead', 'Husband Dead'), ('conference', 'Conference'),
         ('learning', 'Learning')])
    no_of_days = fields.Float('Number Of Days')
    husband_dead_duration_muslim = fields.Float('Husband Dead Duration Muslim')
    husband_dead_duration_non_muslim = fields.Float('Husband Dead Duration Non Muslim')




