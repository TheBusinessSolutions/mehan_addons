# -*- coding: utf-8 -*-

from odoo import api, fields, models
from ast import literal_eval


class HRResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    late_attendance_month_days = fields.Float(string="Late Attendance No. of Month Days")
    late_attendance_time = fields.Float(string="Late Attendance Time")

    def set_values(self):
        super(HRResConfigSettings, self).set_values()
        params = self.env['ir.config_parameter'].sudo()
        params.set_param('n2d_late_attendance.late_attendance_month_days', repr(self.late_attendance_month_days))
        params.set_param('n2d_late_attendance.late_attendance_time', repr(self.late_attendance_time))

    def get_values(self):
        res = super(HRResConfigSettings, self).get_values()
        params = self.env['ir.config_parameter'].sudo()
        res.update(
            late_attendance_month_days=literal_eval(params.get_param('n2d_late_attendance.late_attendance_month_days', 'False')),
            late_attendance_time=literal_eval(params.get_param('n2d_late_attendance.late_attendance_time', 'False')),

        )
        return res

    # def set_values(self):
    #     super(HRResConfigSettings, self).set_values()
    #     params = self.env['ir.config_parameter'].sudo()
    #     params.set_param('n2d_late_attendance.late_attendance_time', repr(self.late_attendance_time))
    #
    # @api.model
    # def get_values(self):
    #     res = super(HRResConfigSettings, self).get_values()
    #     params = self.env['ir.config_parameter'].sudo()
    #     res.update(
    #         late_attendance_time=literal_eval(params.get_param('n2d_late_attendance.late_attendance_time', 'False')),
    #     )
    #     return res
