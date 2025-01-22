# -*- coding: utf-8 -*-

from odoo import models, api, fields

from odoo.exceptions import ValidationError

from datetime import timedelta


class HRLeave(models.Model):
    _inherit = 'hr.leave'

    def _get_number_of_days(self, date_from, date_to, employee_id):
        days = super(HRLeave, self)._get_number_of_days(date_from, date_to, employee_id)
        if employee_id and self.holiday_status_id.allow_days_off:
            employee = self.env["hr.employee"].browse(employee_id)
            if employee.resource_calendar_id:
                work_days = employee.resource_calendar_id._get_weekdays()
                fromdate = fields.Datetime.from_string(date_from)
                todate = fields.Datetime.from_string(date_to)
                days_off = 0
                while fromdate <= todate:
                    if fromdate.weekday() not in work_days:
                        days_off += 1
                    fromdate = fromdate + timedelta(days=1)
                all_days = days + days_off
                return all_days
            else:
                return ValidationError("Please Add Working Schedule In Employee!!")
        else:
            return days

    @api.constrains('date_from', 'date_to', 'number_of_days_temp', 'holiday_status_id')
    def _holidays_validation(self):
        for record in self:
            # print(record.holiday_status_id.leave_type)
            if record.holiday_status_id.leave_type == 'haj':
                if not record.employee_id.hiring_date:
                    raise ValidationError("Please Add Employee Hiring Date")
                diff = (fields.Date.from_string(record.date_from) - fields.Date.from_string(
                    record.employee_id.hiring_date))
                if (diff.days / 365 < 2):
                    raise ValidationError("Employee Service Duration Must Be More Than Two Years")
                res = self.env['hr.leave'].search(
                    [('employee_id', '=', record.employee_id.id), ('holiday_status_id.leave_type', '=', 'haj'),
                     ('state', '=', 'validate')])
                if len(res) > 1:
                    raise ValidationError("HAJ Leave Available Only Once!!")
                if record.number_of_days_temp > record.holiday_status_id.no_of_days:
                    raise ValidationError("Leave Duration Exceed Limit!!")

            elif record.holiday_status_id.leave_type == 'learning':
                if (record.number_of_days_temp > record.holiday_status_id.no_of_days):
                    raise ValidationError(
                        "Leave Duration Must Be Less Than %s days" % record.holiday_status_id.no_of_days)

            elif record.holiday_status_id.leave_type == 'dead':
                if (record.number_of_days_temp > record.holiday_status_id.no_of_days):
                    raise ValidationError(
                        "Leave Duration Must Be Less Than %s days" % record.holiday_status_id.no_of_days)

            elif record.holiday_status_id.leave_type == 'husband_dead':
                if (
                        record.employee_id.is_muslim and record.number_of_days_temp > record.holiday_status_id.husband_dead_duration_muslim):
                    raise ValidationError(
                        "Leave Duration Must Be Less Than %s days" % record.holiday_status_id.husband_dead_duration_muslim)
                elif (
                        not record.employee_id.is_muslim and record.number_of_days_temp > record.holiday_status_id.husband_dead_duration_non_muslim):
                    raise ValidationError(
                        "Leave Duration Must Be Less Than %s days" % record.holiday_status_id.husband_dead_duration_non_muslim)

            elif record.holiday_status_id.leave_type == 'conference':
                if record.number_of_days_temp > record.holiday_status_id.no_of_days:
                    raise ValidationError("Leave Duration Exceed Limit!!")




