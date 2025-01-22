# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HRAbsence(models.Model):
    _name = 'hr.absence'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Absence"

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', string="Status")
    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string="Employee", track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    num_days = fields.Float(string='Number of Days', track_visibility='onchange')

    @api.onchange('employee_id')
    def get_employee_domain(self):
        if self.env.user.has_group('actions_management.actions_group_department_manager'):
            domain = [('parent_id.user_id', '=', self.env.user.id)]
            return {'domain': {'employee_id': domain}}

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.absence')
        return super(HRAbsence, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

