# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HrLeaveType(models.Model):
    _inherit = 'hr.leave.type'


    source = fields.Selection(
        [('excuse', 'Excuse'), ('formal_assignment', 'Formal Assignment'), ('emergency_leave', 'Emergency Leave'),
         ('regular_leave', 'Regular Leave'),('other', 'Other')], default="other")

