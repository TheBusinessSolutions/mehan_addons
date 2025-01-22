# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = 'hr.payslip'

    attend_amount = fields.Float("Absence Amount")
    absence_days = fields.Float("Absence Days")

    def compute_sheet(self):
        for payslip in self:
            payslip.attend_amount, payslip.absence_days = payslip.get_attendance_amount()
        super(HrPayslip, self).compute_sheet()

    def get_attendance_amount(self):
        self.ensure_one()
        attend_days = 0
        total_days = 0
        rate = 0
        for line in self.worked_days_line_ids:
            if line.code == 'Attend':
                attend_days = line.number_of_days
            elif line.code == 'WORK100':
                total_days = line.number_of_days
        if total_days:
            rate = 1 - (attend_days / total_days)
        if not self.contract_id:
            raise ValidationError("Please Add Contract!")
        return rate * self.contract_id.wage, total_days - attend_days

    @api.model
    def get_worked_day_lines(self, contracts, date_from, date_to):
        res = super(HrPayslip, self).get_worked_day_lines(contracts, date_from, date_to)
        print('rrrrrrrrrrr')
        vals = self.employee_id.get_absense_days(date_from, date_to)
        res.append(vals)
        return res
