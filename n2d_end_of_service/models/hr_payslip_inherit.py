# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    eos_amount = fields.Float("E.O.S Allowances")

    def compute_sheet(self):
        for rec in self:
            rec.eos_amount = rec.compute_eos_amount()
        super(HrPayslip, self).compute_sheet()

    def compute_eos_amount(self):
        self.ensure_one()
        eos_ids = self.env['employee.eos'].search(
            [('employee_id', '=', self.employee_id.id), ('date', '>=', self.date_from),
             ('date', '<=', self.date_to)])

        total = 0
        for eos_obj in eos_ids:
            if eos_obj.state == 'confirmed' or eos_obj.payslip_id.id == self.id:
                total += eos_obj.amount
                eos_obj.action_done()
                eos_obj.payslip_id = self.id
        return total
