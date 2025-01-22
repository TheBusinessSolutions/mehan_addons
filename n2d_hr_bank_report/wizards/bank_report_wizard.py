# -*- encoding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EmployeeDataWizard(models.TransientModel):
    _name = 'bank.report.wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    bank_id = fields.Many2one('res.bank', string='Bank Name')
    account_number = fields.Char()
    results = fields.Many2many(comodel_name="hr.payslip")


    def get_data(self):
        self.ensure_one()
        domain = [('state', '=', 'done')]
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))
        if self.date_from:
            domain.append(('date_from', '>=', self.date_from))
        if self.date_to:
            domain.append(('date_to', '<=', self.date_to))
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValidationError("Date To Must Be Greater Than Date From")
        payslip_ids = self.env['hr.payslip'].search(domain)
        if not payslip_ids:
            raise ValidationError("No Data Available!!")
        self.results = payslip_ids
        return self.env.ref('n2d_hr_bank_report.action_report_bank').report_action(self)

    @api.onchange('bank_id', 'employee_id')
    def get_acc_number(self):
        for rec in self:
            rec.account_number = False
            if rec.employee_id:
                for line in rec.employee_id.employee_bank_ids:
                    if line.bank_id.id == rec.bank_id.id:
                        rec.account_number = line.acc_number


    @api.onchange('employee_id')
    def get_bank(self):
        for rec in self:
            if rec.employee_id:
                rec.bank_id = rec.employee_id.bank_account_id.bank_id



class HrEmployee(models.Model):

    _inherit = 'hr.employee'


    @api.onchange('bank_account_id')
    def get_bank_domain(self):
        for rec in self:
            banks = []
            for line in rec.employee_bank_ids:
                banks.append(line.bank_id.id)

            domain = [('bank_id', 'in', banks)]
            return {'domain': {'bank_account_id': domain}}