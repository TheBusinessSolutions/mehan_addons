# -*- encoding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class EmployeeSiteDataWizard(models.TransientModel):
    _name = 'site.allowance.wizard'

    employee_id = fields.Many2one('hr.employee', string='Employee Name')
    date_from = fields.Date('Date From')
    date_to = fields.Date('Date To')
    site_id = fields.Many2one('company.location', string='Site Name')

    def get_data(self):
        self.ensure_one()
        domain = []
        if self.employee_id:
            domain.append(('employee_id', '=', self.employee_id.id))
        if self.site_id:
            domain.append(('site_id', '=', self.site_id.id))
        if self.date_from:
            domain.append(('check_in', '>=', self.date_from))
        if self.date_to:
            domain.append(('check_in', '<=', self.date_to))
        if self.date_from and self.date_to and self.date_to < self.date_from:
            raise ValidationError("Date To Must Be Greater Than Date From")
        attendance_ids = self.env['hr.attendance'].search(domain)
        if not attendance_ids:
            raise ValidationError("No Data Available!!")
        data = self.read()[0]
        data['ids'] = attendance_ids
        datas = {'form': data}
        return self.env.ref('hr_site_allowance.action_report_employee_site').with_context(date_from=self.date_from, date_to=self.date_to).report_action(docids=attendance_ids)
