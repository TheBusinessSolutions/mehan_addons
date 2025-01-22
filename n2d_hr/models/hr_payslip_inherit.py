# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import date, datetime, time
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from pytz import timezone
from pytz import utc


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    overtime_amount = fields.Float("Overtime")
    total_overtime_hours = fields.Float("Total Overtime", readonly=True)
    absence_amount = fields.Float("Absence")
    penalty_amount = fields.Float("Penalty")
    bonus_amount = fields.Float("Penalty")
    department_id = fields.Many2one(string='Department', related='employee_id.department_id')

    @api.constrains('employee_id', 'date_from', 'date_to')
    def prevent_dub(self):
        for rec in self:
            payslips = self.env['hr.payslip'].search(
                [('employee_id', '=', rec.employee_id.id), ('date_from', '=', rec.date_from),
                 ('date_to', '=', rec.date_to)])
            if len(payslips) > 1:
                raise ValidationError("You Cant Create More Than One Payslip In Same Month!!")

    def copy(self, default=None):
        raise ValidationError("You Can't Duplicate Payslip!!")

    def compute_sheet(self):
        for rec in self:
            rec.overtime_amount, rec.total_overtime_hours = rec.compute_overtime_amount()
            rec.absence_amount = rec.compute_absence_amount()
            rec.penalty_amount = rec.compute_penalty_amount()
            rec.bonus_amount = rec.compute_bonus_amount()
        super(HrPayslip, self).compute_sheet()

    def compute_overtime_amount(self):
        self.ensure_one()
        over_time_ids = self.env['hr.overtime'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'confirmed'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        month_days = float(self.env['ir.config_parameter'].sudo().get_param('n2d_hr.attendance_month_days'))
        if month_days <= 0:
            raise ValidationError("Please set Month Days For Absence/Overtime in payroll configuration!!")

        rate = float(self.env['ir.config_parameter'].sudo().get_param('n2d_hr.overtime_rate'))
        if rate <= 0:
            raise ValidationError("Please set overtime rate in payroll configuration!!")
        total = 0
        total_overtime = 0
        if self.contract_id and self.contract_id.wage > 0:
            hour_rate = (self.contract_id.wage / month_days) / 8
            for overtime in over_time_ids:
                total += overtime.num_hours
                total_overtime += overtime.num_hours

            total = hour_rate * rate * total
        return total, total_overtime

    def compute_absence_amount(self):
        self.ensure_one()
        absence_ids = self.env['hr.absence'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'confirmed'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        month_days = float(self.env['ir.config_parameter'].sudo().get_param('n2d_hr.attendance_month_days'))
        if month_days <= 0:
            raise ValidationError("Please set Month Days For Absence/Overtime in payroll configuration!!")

        rate = float(self.env['ir.config_parameter'].sudo().get_param('n2d_hr.absence_rate'))
        if rate <= 0:
            raise ValidationError("Please set Absence rate in payroll configuration!!")
        total = 0
        if self.contract_id and self.contract_id.wage > 0:
            day_rate = (self.contract_id.total_wage / month_days)
            for absence in absence_ids:
                total += absence.num_days
            total = day_rate * rate * total
        return total

    def compute_penalty_amount(self):
        self.ensure_one()
        penalty_ids = self.env['hr.penalty'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'confirmed'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        total = 0

        for penlity in penalty_ids:
            total += penlity.amount
        return total

    def compute_bonus_amount(self):
        self.ensure_one()
        bonus_ids = self.env['hr.bonus'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'confirmed'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        total = 0

        for bon in bonus_ids:
            total += bon.amount
        return total

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):

        """
        @param contract: Browse record of contracts
        @return: returns a list of dict containing the input that should be applied for the given contract between date_from and date_to
        """
        res = []
        # fill only if the contract as a working schedule linked
        for contract in contracts.filtered(lambda contract: contract.resource_calendar_id):
            day_from = datetime.combine(fields.Date.from_string(date_from), time.min)
            day_to = datetime.combine(fields.Date.from_string(date_to), time.max)

            # compute leave days
            leaves = {}
            calendar = contract.resource_calendar_id
            tz = timezone(calendar.tz)
            day_leave_intervals = contract.employee_id.list_leaves(day_from, day_to,
                                                                   calendar=contract.resource_calendar_id)
            for day, hours, leave in day_leave_intervals:
                holiday = leave.holiday_id
                current_leave_struct = leaves.setdefault(holiday.holiday_status_id, {
                    'name': holiday.holiday_status_id.name or _('Global Leaves'),
                    'sequence': 5,
                    'code': holiday.holiday_status_id.code or 'GLOBAL',
                    'number_of_days': 0.0,
                    'number_of_hours': 0.0,
                    'contract_id': contract.id,
                })
                current_leave_struct['number_of_hours'] += hours
                work_hours = calendar.get_work_hours_count(
                    tz.localize(datetime.combine(day, time.min)),
                    tz.localize(datetime.combine(day, time.max)),
                    compute_leaves=False,
                )
                if work_hours:
                    current_leave_struct['number_of_days'] += hours / work_hours

            # compute worked days
            work_data = contract.employee_id.get_work_days_data(day_from, day_to,
                                                                calendar=contract.resource_calendar_id)
            month_days = self.env['ir.config_parameter'].sudo().get_param('n2d_hr.attendance_month_days')
            hours_day = contract.resource_calendar_id.hours_per_day
            print(month_days)
            print(hours_day)

            attendances = {
                'name': _("Normal Working Days paid at 100%"),
                'sequence': 1,
                'code': 'WORK100',
                'number_of_days': month_days,
                'number_of_hours': float(month_days) * float(hours_day),
                'contract_id': contract.id,
            }

            res.append(attendances)
            res.extend(leaves.values())
        return res
