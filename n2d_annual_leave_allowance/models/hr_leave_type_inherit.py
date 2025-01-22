# -*- coding: utf-8 -*-

from odoo import models, fields


class HRHolidayStatus(models.Model):
    _inherit = 'hr.leave.type'

    is_legal = fields.Boolean("Legal Leave")

