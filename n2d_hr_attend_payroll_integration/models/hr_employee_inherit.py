# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from datetime import datetime
import pytz
import calendar


class Employee(models.Model):
    _inherit = 'hr.employee'

    finger_print_id = fields.Char("Finger Print ID")

    def get_absense_days(self, date_from, date_to):
        print('Absense')
        self.ensure_one()

        values = [('0', 'Monday'), ('1', 'Tuesday'), ('2', 'Wednesday'), ('3', 'Thursday'),
                  ('4', 'Friday'),
                  ('5', 'Saturday'), ('6', 'Sunday')]

        attendance_obj = self.env['hr.attendance']
        attendances = attendance_obj.search([('employee_id', '=', self.id)])
        date_from = fields.Date.from_string(date_from)
        date_to = fields.Date.from_string(date_to)
        # ('dayofweek', '=', str(now.weekday())
        total_hours = 0
        day_hours = 8
        employee_calendar = calendar or self.resource_calendar_id
        for attendance in attendances:
            if attendance.check_in and attendance.check_out and attendance.check_in.date() >= date_from and attendance.check_out.date() <= date_to:
                print("attendance.check_in", attendance.check_in)
                for workday in self.resource_calendar_id.attendance_ids:
                    if calendar.day_name[attendance.check_in.weekday()] == dict(values)[workday.dayofweek]:
                        if attendance.check_in.date() == attendance.check_out.date():

                            total_hours += attendance.worked_hours
                            # day_hours = self.get_day_work_hours_count(fields.Datetime.from_string(attendance.check_in).date()) or 8
                            day_hours = 8


        attendance_values = {
            'name': _("Attendance Days"),
            'sequence': 1,
            'code': 'Attend',
            'number_of_days': (round((total_hours / day_hours )*4)/4),
            'number_of_hours': (round(total_hours*4)/4),
            'contract_id': self.contract_id.id
        }
        return attendance_values