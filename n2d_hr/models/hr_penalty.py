# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HRPenalty(models.Model):
    _name = 'hr.penalty'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Penalty"

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', string="Status")
    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string="Employee", track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    type_id = fields.Many2one('hr.penalty.confg', "Type", ondelete="restrict")
    amount = fields.Float('Deduction Amount')

    @api.onchange('employee_id')
    def get_employee_domain(self):
        if self.env.user.has_group('actions_management.actions_group_department_manager'):
            domain = [('parent_id.user_id', '=', self.env.user.id)]
            return {'domain': {'employee_id': domain}}

    @api.depends('type_id')
    @api.onchange('type_id')
    def get_deduction_amount(self):
        for rec in self:
            rec.amount = rec.type_id.penalty_amount

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.penalty')
        return super(HRPenalty, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'