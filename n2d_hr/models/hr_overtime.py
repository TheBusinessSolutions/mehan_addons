# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HROvertime(models.Model):
    _name = 'hr.overtime'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Overtime"

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', string="Status")
    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string="Employee",  track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    time_from = fields.Float(string='Date From')
    time_to = fields.Float(string='Date To')
    num_hours = fields.Float(string='Number of Hours', track_visibility='onchange')
    officer_id = fields.Many2one('hr.employee', related='employee_id.parent_id', string='Officer')

    @api.onchange('employee_id')
    def get_employee_domain(self):
        if self.env.user.has_group('actions_management.actions_group_department_manager'):
            domain = [('parent_id.user_id', '=', self.env.user.id)]
            return {'domain': {'employee_id': domain}}

    @api.onchange('time_from', 'time_to')
    def get_hours(self):
        for rec in self:
            rec.num_hours = rec.time_to - rec.time_from

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.overtime')
        return super(HROvertime, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'
