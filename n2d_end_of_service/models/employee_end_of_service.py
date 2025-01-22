# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError


class EmployeeEOS(models.Model):
    _name = 'employee.eos'
    _rec_name = 'employee_id'

    state = fields.Selection(
        [('draft', 'Draft'), ('confirmed', 'Confirmed'), ('done', 'Done'), ('cancelled', 'Cancelled')], default='draft')
    employee_id = fields.Many2one('hr.employee', "Employee")
    amount = fields.Float("E.O.S Amount", compute='get_eos_amount', store=True)
    date = fields.Date("Date")
    reason_id = fields.Many2one("eos.reason", "Reason")
    payslip_id = fields.Many2one('hr.payslip', "Payroll", copy=False)
    journal_id = fields.Many2one('account.journal', "Journal")
    move_id = fields.Many2one('account.move', "Entry", copy=False)

    vacations_balance = fields.Float("Vacations Balance" , related='employee_id.leaves_count')
    remaining_loan = fields.Float("Remaining Loan" , compute = 'compute_loan_amount')
    net_payment_amount = fields.Float("Net Payment Amount", compute='calc_total_amount')
    calculate_loan = fields.Boolean("Calculate Loan?")

    starting_from = fields.Date("Starting From")
    to = fields.Date("To")


    def calc_total_amount(self):
        self.ensure_one()
        total = self.amount
        if self.calculate_loan:
            total -= self.remaining_loan
        self.net_payment_amount = total

    def action_done(self):
        debit_id = int(self.env['ir.config_parameter'].sudo().get_param('n2d_end_of_service.eos_debit_id'))
        credit_id = int(self.env['ir.config_parameter'].sudo().get_param('n2d_end_of_service.eos_credit_id'))
        if not debit_id:
            raise ValidationError("Please Add Debit Account In Configuration")
        if not credit_id:
            raise ValidationError("Please Add Credit Account In Configuration")
        for rec in self:
            move = self.env['account.move'].create({
                'name': '/',
                'journal_id': rec.journal_id.id,
                'date': rec.date,
                'ref': 'End Of Service' + rec.employee_id.display_name,
                'line_ids': [(0, 0, {
                    'name': 'End Of Service',
                    'debit': rec.net_payment_amount,
                    'account_id': debit_id,
                }), (0, 0, {
                    'name': 'End Of Service',
                    'credit': rec.net_payment_amount,
                    'account_id': credit_id,
                })]
            })
            rec.move_id = move.id
            move.post()
            rec.state = 'done'

    def compute_leave_allowances(self):
        self.ensure_one()
        month_days = float(self.env['ir.config_parameter'].sudo().get_param('n2d_end_of_service.eos_month_days'))
        print("Month Days --------------------------------- ", month_days)
        if month_days <= 0:
            raise ValidationError("Please set Month Days in payroll configuration!!")
        total = 0.0
        if self.employee_id.contract_id and self.employee_id.contract_id.wage > 0:
            day_rate = (self.employee_id.contract_id.wage / month_days)
            total = day_rate * self.vacations_balance
        return round(total, 3)

    def get_last_leave(self):
        self.ensure_one()
        leave = self.env['hr.holidays'].search(
            [('employee_id', '=', self.employee_id.id), ('type', '=', 'remove')], limit=1)
        return leave


    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    def action_cancel(self):
        for rec in self:
            rec.payslip_id = False
            rec.state = 'cancelled'

    @api.depends('reason_id', 'employee_id', 'date')
    def get_eos_amount(self):
        for rec in self:
            if rec.employee_id.contract_id and rec.reason_id and rec.reason_id.calc_eos and rec.date:
                month_days = float(
                    self.env['ir.config_parameter'].sudo().get_param('n2d_end_of_service.eos_month_days'))
                if not month_days:
                    raise ValidationError("Please Add E.O.S Month Days In Payroll Settings!")
                if not rec.employee_id.hiring_date:
                    raise ValidationError(("Please Add Hiring Date For %s !!") % rec.employee_id.display_name)
                years = relativedelta(fields.Date.from_string(rec.date),
                                      fields.Date.from_string(rec.employee_id.hiring_date)).years
                duration = years + (relativedelta(fields.Date.from_string(rec.date),
                                                  fields.Date.from_string(rec.employee_id.hiring_date)).months / 12)
                day_rate = rec.employee_id.contract_id.wage / month_days
                if rec.employee_id.contract_id.contract_type == 'limited':
                    if rec.employee_id.contract_id.payment_type in ['hourly', 'daily', 'weekly', 'by_unit']:
                        max_eos = rec.employee_id.contract_id.wage * 12
                        amount = 0.0
                        if duration <= 5:
                            amount = 10 * day_rate * duration
                            if amount > max_eos:
                                amount = max_eos
                        else:
                            amount = 15 * day_rate * duration
                            if amount > max_eos:
                                amount = max_eos
                        rec.amount = amount
                    elif rec.employee_id.contract_id.payment_type == 'monthly':
                        max_eos = rec.employee_id.contract_id.wage * 18
                        amount = 0.0
                        if duration <= 5:
                            amount = 15 * day_rate * duration
                            if amount > max_eos:
                                amount = max_eos
                        else:
                            amount = 30 * day_rate * duration
                            if amount > max_eos:
                                amount = max_eos
                        rec.amount = amount
                elif rec.employee_id.contract_id.contract_type == 'unlimited':
                    if rec.employee_id.contract_id.payment_type in ['hourly', 'daily', 'weekly', 'by_unit']:
                        amount = 0.0
                        if 3 <= duration <= 5:
                            amount = 0.5 * 10 * day_rate * duration
                        elif duration > 5:
                            amount = 0.75 * 15 * day_rate * duration
                        rec.amount = amount
                    elif rec.employee_id.contract_id.payment_type == 'monthly':
                        amount = 0.0
                        if 3 <= duration <= 5:
                            amount = 0.5 * 15 * day_rate * duration
                        elif duration > 5:
                            amount = 0.75 * 30 * day_rate * duration
                        rec.amount = amount

            else:
                rec.amount = 0.0

    def compute_loan_amount(self):
        self.ensure_one()
        employee_loan = self.env['hr.loan'].search([('employee_id' , '=' , self.employee_id.id),('state' , '=' , 'approve')])

        all_amount_loan = 0

        for loan in employee_loan:
            for line in loan.loan_lines:
                if (line.paid == False and line.date >= self.date):
                    all_amount_loan += line.amount
        self.remaining_loan = all_amount_loan
