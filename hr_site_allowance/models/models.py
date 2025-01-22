# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _



class SiteAllowance(models.Model):
    _name = 'site.allowance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'site.allowance'
    _order = 'create_date DESC'

    site_id = fields.Many2one('company.location', string='Site')
    name = fields.Float('Allowance')



class HRAttendance(models.Model):
    _inherit = 'hr.attendance'

    site_id = fields.Many2one('company.location', string='Site')
    site_allowance = fields.Float('Allowance', compute='_get_site_allowance')



    @api.depends('site_id')
    def _get_site_allowance(self):
        for rec in self:
            site_allowance_value = self.env['site.allowance'].search([('site_id', '=', rec.site_id.id)]).name
            rec.site_allowance = site_allowance_value



class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    site_ids = fields.Many2many('company.location', 'employee_site_rel', 'employee', 'site', string='Site')




class HrPayslip(models.Model):
    _inherit = "hr.payslip"

    site_allowance_amount = fields.Float("Site Allowance")

    def compute_sheet(self):
        for rec in self:
            rec.site_allowance_amount = rec.compute_site_allowance_amount()
        super(HrPayslip, self).compute_sheet()

    def compute_site_allowance_amount(self):
        self.ensure_one()
        allowance_ids = self.env['hr.attendance'].search(
            [('employee_id', '=', self.employee_id.id), ('check_in', '>=', self.date_from),
             ('check_in', '<=', self.date_to)])
        total = 0

        for alw in allowance_ids:
            total += alw.site_allowance
        return total
