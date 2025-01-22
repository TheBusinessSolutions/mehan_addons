# -*- coding: utf-8 -*-

import time
from datetime import datetime,date
from dateutil import relativedelta
from odoo import models, fields, api, _


class EmployeeInsurance(models.Model):
    _name = 'hr.insurance'
    _description = 'HR Insurance'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True, help="Employee")
    policy_id = fields.Many2one('insurance.policy', string='Policy', required=True, help="Policy")
    company_percentage = fields.Float(required=True, help="Policy amount")
    employee_percentage = fields.Float(required=True, help="Policy amount")
    sum_insured = fields.Float(string="Sum Insured", required=True, help="Insured sum")
    policy_coverage = fields.Selection([('monthly', 'Monthly'), ('yearly', 'Yearly')],
                                       required=True, default='yearly',
                                       string='Policy Coverage', help="During of the policy", readonly=True)
    date_from = fields.Date(string='Date From',
                            default=time.strftime('%Y-%m-%d'), help="Start date")
    date_to = fields.Date(string='Date To',   readonly=True, help="End date")
    state = fields.Selection([('active', 'Active'),
                              ('expired', 'Expired'), ],
                             default='active', string="State",compute='get_status')
    company_id = fields.Many2one('res.company', string='Company', required=True, help="Company",
                                 default=lambda self: self.env.user.company_id)
    insurance_number = fields.Char('Insurance Number')


    def get_status(self):
        current_datetime = datetime.now()
        current_date = datetime.strftime(current_datetime, "%Y-%m-%d ")
        for i in self:
            # x = str(i.date_from)
            y = str(i.date_to)
            # if x <= current_date:
            if y >= current_date:
                i.state = 'active'
            else:
                i.state = 'expired'

    # @api.constrains('policy_coverage')
    # @api.onchange('policy_coverage')
    # def get_policy_period(self):
    #     if self.policy_coverage == 'monthly':
    #         self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+1, day=1, days=-1))[:10]
    #     if self.policy_coverage == 'yearly':
    #         self.date_to = str(datetime.now() + relativedelta.relativedelta(months=+12))[:10]

    @api.onchange('date_from')
    def get_date_to(self):
        if self.date_from:
            self.date_to = str(self.date_from + relativedelta.relativedelta(months=+12))[:10]

    @api.onchange('employee_id')
    def get_employee_insurance(self):
        for rec in self:
            rec.company_percentage = rec.employee_id.company_insurance_percentage
            rec.employee_percentage = rec.employee_id.employee_insurance_percentage




class HrInsurance(models.Model):
    _inherit = 'hr.employee'

    company_insurance_percentage = fields.Float(related='contract_id.company_insurance_percentage')
    employee_insurance_percentage = fields.Float(related='contract_id.employee_insurance_percentage')
    subscription_fee = fields.Float(compute="get_subscription_fee")
    deduced_amount_per_month = fields.Float(string="Salary deduced per month", compute="get_deduced_amount", help="Amount that is deduced from the salary per month")
    deduced_amount_per_year = fields.Float(string="Salary deduced per year", compute="get_deduced_amount", help="Amount that is deduced fronm the salary per year")
    company_amount_per_month = fields.Float(string="Company amount per month", compute="get_deduced_amount")
    company_amount_per_year = fields.Float(string="Company amount per year", compute="get_deduced_amount")
    insurance = fields.One2many('hr.insurance', 'employee_id', string="Insurance", help="Insurance",
                                domain=[('state', '=', 'active')])


    @api.depends('subscription_fee')
    def get_deduced_amount(self):
        current_date = datetime.now()
        current_datetime = datetime.strftime(current_date, "%Y-%m-%d ")
        for emp in self:
            emp_ins_amount = 0
            comp_ins_amount = 0
            for ins in emp.insurance:
                x = str(ins.date_from)
                y = str(ins.date_to)
                if x < current_datetime:
                    if y > current_datetime:
                        if ins.policy_coverage == 'yearly':
                            emp_ins_amount = emp_ins_amount + ins.employee_percentage
                            comp_ins_amount = comp_ins_amount + ins.company_percentage
            emp.deduced_amount_per_month = emp.subscription_fee * emp_ins_amount / 100
            emp.company_amount_per_month = emp.subscription_fee * comp_ins_amount / 100
            emp.deduced_amount_per_year = emp.deduced_amount_per_month * 12
            emp.company_amount_per_year = emp.company_amount_per_month * 12

    def get_subscription_fee(self):
        for rec in self:
            rec.subscription_fee = 0.0
            if rec.insurance:
                for line in rec.insurance:
                    if line.state == 'active':
                        rec.subscription_fee += line.sum_insured

class InsuranceRuleInput(models.Model):
    _inherit = 'hr.payslip'

    def get_inputs(self, contract_ids, date_from, date_to):
        res = super(InsuranceRuleInput, self).get_inputs(contract_ids, date_from, date_to)
        contract_obj = self.env['hr.contract']
        for i in contract_ids:
            if contract_ids[0]:
                emp_id = contract_obj.browse(i[0].id).employee_id
                for result in res:
                    if emp_id.deduced_amount_per_month != 0:
                        if result.get('code') == 'INSUR':
                            result['amount'] = emp_id.deduced_amount_per_month
        return res


class HRContract(models.Model):
    _inherit = 'hr.contract'

    company_insurance_percentage = fields.Float()
    employee_insurance_percentage = fields.Float()
