# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from ast import literal_eval


class HRResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    overtime_rate = fields.Float(string="Overtime Rate")
    absence_rate = fields.Float(string="Absence Rate")
    attendance_month_days = fields.Float(string="Absence/Overtime No. of Month Days")
    identification_alert_days = fields.Integer(string='Identification Alert Days', config_parameter='n2d_hr.identification_alert')
    passport_alert_days = fields.Integer(string='Passport Alert Days', config_parameter='n2d_hr.passport_alert')

    def set_values(self):
        super(HRResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('n2d_hr.attendance_month_days', repr(self.attendance_month_days))
        params.set_param('n2d_hr.overtime_rate', repr(self.overtime_rate))
        params.set_param('n2d_hr.absence_rate', repr(self.absence_rate))


    @api.model
    def get_values(self):
        res = super(HRResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            attendance_month_days=literal_eval(params.get_param('n2d_hr.attendance_month_days', 'False')),
            overtime_rate=literal_eval(params.get_param('n2d_hr.overtime_rate', 'False')),
            absence_rate=literal_eval(params.get_param('n2d_hr.absence_rate', 'False')),
        )
        return res