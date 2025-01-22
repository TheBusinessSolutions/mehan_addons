# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    leave_allowances_amount = fields.Float("Leave Allowances")

    def compute_sheet(self):
        for rec in self:
            rec.leave_allowances_amount = rec.compute_leave_allowances()
        super(HrPayslip, self).compute_sheet()

    def compute_leave_allowances(self):
        self.ensure_one()
        leave_allowances_ids = self.env['annual.leave.allowances'].search(
            [('employee_id', '=', self.employee_id.id), ('state', '=', 'confirmed'), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])
        month_days = float(self.env['ir.config_parameter'].sudo().get_param('n2d_annual_leave_allowance.month_days'))
        if month_days <= 0:
            raise ValidationError("Please set Month Days in payroll configuration!!")
        total = 0
        if self.contract_id and self.contract_id.wage > 0:
            day_rate = (self.contract_id.wage / month_days)
            for leave_all in leave_allowances_ids:
                total += leave_all.no_of_days
                leave_all.action_done()
            total = day_rate * total
        return total
