# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AnnualLeaveAllowances(models.Model):
    _name = 'annual.leave.allowances'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    state = fields.Selection(
        [('draft', "Draft"), ('confirmed', "Confirmed"), ('done', "Done"), ('rejected', "Rejected")],
        default='draft')
    employee_id = fields.Many2one('hr.employee', "Employee")
    no_of_days = fields.Float("Requested Days")
    date = fields.Date("Date")
    journal_id = fields.Many2one('account.journal', "Journal")
    move_id = fields.Many2one('account.move', "Entry", copy=False)

    vacations_balance = fields.Float("Vacations Balance" , compute='calc_leave_balance')
    remaining_balance = fields.Float("Remaining Balance", related='employee_id.leaves_count')
    remaining_loan = fields.Float("Remaining Loan" , compute = 'compute_loan_amount')
    net_payment_amount = fields.Float("Net Payment Amount", compute='calc_total_amount')
    calculate_loan = fields.Boolean("Calculate Loan?")

    starting_from = fields.Date("Starting From")
    to = fields.Date("To")

    def calc_leave_balance(self):
        self.ensure_one()
        self.vacations_balance = self.remaining_balance - self.no_of_days

    def calc_total_amount(self):
        self.ensure_one()
        total = self.compute_leave_allowances()
        if self.calculate_loan:
            total -= self.remaining_loan
        self.net_payment_amount = total
    def action_done(self):
        debit_id = int(self.env['ir.config_parameter'].sudo().get_param('n2d_annual_leave_allowance.leave_debit_id'))
        credit_id = int(self.env['ir.config_parameter'].sudo().get_param('n2d_annual_leave_allowance.leave_credit_id'))
        if not debit_id:
            raise ValidationError("Please Add Debit Account In Configuration")
        if not credit_id:
            raise ValidationError("Please Add Credit Account In Configuration")
        for rec in self:
            move = self.env['account.move'].create({
                'name': '/',
                'journal_id': rec.journal_id.id,
                'date': rec.date,
                'ref': 'Leave Allowances' + rec.employee_id.display_name,
                'line_ids': [(0, 0, {
                    'name': 'Leave Allowances',
                    'debit': rec.net_payment_amount,
                    'account_id': debit_id,
                }), (0, 0, {
                    'name': 'Leave Allowances',
                    'credit': rec.net_payment_amount,
                    'account_id': credit_id,
                })]
            })
            rec.move_id = move.id
            move.post()
            rec.state = 'done'

    def compute_leave_allowances(self):
        self.ensure_one()
        month_days = float(self.env['ir.config_parameter'].sudo().get_param('n2d_annual_leave_allowance.month_days'))
        if month_days <= 0:
            raise ValidationError("Please set Month Days in payroll configuration!!")
        total = 0.0
        if self.employee_id.contract_id and self.employee_id.contract_id.wage > 0:
            day_rate = (self.employee_id.contract_id.wage / month_days)
            total = day_rate * self.no_of_days
        return round(total, 3)

    @api.constrains('employee_id', 'date', 'no_of_days')
    def validate_leaves(self):
        for rec in self:
            legal = self.env['hr.leave.type'].search([('is_legal', '=', True)], limit=1)
            if legal:
                leave_days = legal.get_days(rec.employee_id.id)[legal.id]
                if leave_days['remaining_leaves'] < rec.no_of_days:
                    raise ValidationError("Employee Don't Have This Number of Days!!")
            else:
                raise ValidationError("There Are No Legal Leaves!!")

    def get_last_leave(self):
        self.ensure_one()
        leave = self.env['hr.leave'].search(
            [('employee_id', '=', self.employee_id.id), ('type', '=', 'remove')], limit=1)
        return leave

    def action_confirm(self):
        for rec in self:
            legal = self.env['hr.leave.type'].search([('is_legal', '=', True)], limit=1)
            allocation = self.env['hr.leave'].search(
                [('holiday_status_id', '=', legal.id), ('employee_id', '=', rec.employee_id.id), ('type', '=', 'add')],
                limit=1)
            if allocation:
                allocation.number_of_days_temp = allocation.number_of_days_temp - rec.no_of_days
            else:
                raise ValidationError("Can't Find Allocation!!")
            rec.state = 'confirmed'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'

    def compute_loan_amount(self):
        self.ensure_one()
        employee_loan = self.env['hr.loan'].search([('employee_id' , '=' , self.employee_id.id),('state' , '=' , 'approve')])

        all_amount_loan = 0

        for loan in employee_loan:
            for line in loan.loan_lines:
                if (line.paid == False and line.date >= self.date):
                    all_amount_loan += line.amount
        self.remaining_loan = all_amount_loan

