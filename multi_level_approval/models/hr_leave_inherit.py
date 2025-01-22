# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HrLeave(models.Model):
    _inherit = 'hr.leave'

    attachment = fields.Binary('Attachment', attachment=True)
    address = fields.Char("Address")
    mobile = fields.Char("Mobile")
    sign = fields.Selection(
        [('no_sign_in', 'No Sign In'),
         ('no_sign_out', 'No Sign Out'),
         ('no_sign_in_out', 'No Sign In/Out'),
         ], string="Attendance status", default='no_sign_in_out')

    source = fields.Selection([('excuse', 'Excuse'), ('formal_assignment', 'Formal Assignment'), ('emergency_leave', 'Emergency Leave'), ('regular_leave', 'Regular Leave'), ('other', 'Other')], default="other")

    @api.model
    def default_get(self, fields_list):
        defaults = super(HrLeave, self).default_get(fields_list)

        defaults['holiday_status_id'] = False
        return defaults

    @api.onchange('holiday_status_id')
    @api.depends('holiday_status_id')
    def onchance_holiday_status_id(self):
        for rec in self:
            if rec.leave_type_request_unit == 'hour':
                rec.request_unit_hours = True
            else:
                rec.request_unit_hours = False

    @api.constrains('holiday_status_id')
    def check_emergency_leave(self):
        for rec in self:
            if rec.holiday_status_id.source == 'emergency_leave' and rec.number_of_dayes > 1:
                raise ValueError('! Not Allowed to take more than one Day.')