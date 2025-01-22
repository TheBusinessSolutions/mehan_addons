# -*- encoding: utf-8 -*-

from odoo import models, fields, api
import pytz



class HRAttendance(models.Model):
    _inherit = 'hr.attendance'


    def write(self, values):
        res = super(HRAttendance, self).write(values)
        for rec in self:
            if rec.check_out:
                check_out_day = rec.check_out.strftime("%A")
                user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
                check_out_zone_time = pytz.utc.localize(rec.check_out).astimezone(user_tz)
                check_out_time = rec.conv_time_float(check_out_zone_time.strftime("%H:%M"))
                attendance = rec.employee_id.contract_id.resource_calendar_id.attendance_ids
                for line in attendance:
                    dayweek = dict(line._fields['dayofweek'].selection).get(line.dayofweek)
                    if check_out_day == dayweek:
                        if check_out_time > line.hour_to:
                            vals = {
                                'employee_id': rec.employee_id.id,
                                'date': rec.check_out.date(),
                                'time_from': line.hour_to,
                                'time_to': check_out_time,
                                'num_hours': check_out_time - line.hour_to,
                            }
                            employee_overtime = self.env['hr.overtime'].sudo().create(vals)

        return res

    def conv_time_float(self, value):
        vals = value.split(':')
        t, hours = divmod(float(vals[0]), 24)
        t, minutes = divmod(float(vals[1]), 60)
        minutes = minutes / 60.0
        return hours + minutes