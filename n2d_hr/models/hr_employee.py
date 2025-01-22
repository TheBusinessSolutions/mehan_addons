# -*- coding: utf-8 -*-

from odoo import models, fields

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    status = fields.Selection([('company', 'Company'), ('outside_company', 'Outside Company')])
    unified_number = fields.Char('Unified Number')
    bank_visa_id = fields.Many2one('bank.visa', string='Visa')
    identification_expire_date = fields.Date('Identification Expire Date')
    passport_expire_date = fields.Date('Passport Expire Date')
    employee_bank_ids = fields.One2many('hr.employee.bank', 'employee_id')


class BankVisa(models.Model):
    _name = 'bank.visa'


    name = fields.Char()


class HrEmployeeBank(models.Model):
    _name = 'hr.employee.bank'

    employee_id = fields.Many2one('hr.employee')
    bank_id = fields.Many2one('res.bank')
    acc_number = fields.Char()
