# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HRBonus(models.Model):
    _name = 'hr.bonus'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Bonus"

    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirmed')], default='draft', string="Status")
    name = fields.Char("Name")
    employee_id = fields.Many2one('hr.employee', string="Employee", track_visibility='onchange')
    date = fields.Date(string='Date', track_visibility='onchange')
    type_id = fields.Many2one('hr.bonus.confg', "Type", ondelete="restrict")
    amount = fields.Float('Bonus Amount')

    @api.onchange('employee_id')
    def get_employee_domain(self):
        if self.env.user.has_group('actions_management.actions_group_department_manager'):
            domain = [('parent_id.user_id', '=', self.env.user.id)]
            return {'domain': {'employee_id': domain}}

    @api.depends('type_id')
    @api.onchange('type_id')
    def get_bonus_amount(self):
        for rec in self:
            rec.amount = rec.type_id.bonus_amount

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('hr.bonus')
        return super(HRBonus, self).create(vals)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'