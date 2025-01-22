# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class HrAttendance(models.Model):
    _name = 'hr.attendance'
    _inherit = ['hr.attendance','mail.thread']

    finger_print_id = fields.Char("Finger Print ID")

    @api.onchange('finger_print_id')
    @api.depends('finger_print_id')
    def get_employee_id(self):
        for rec in self:
            if rec.finger_print_id:
                employee_id = self.env['hr.employee'].search([('finger_print_id', '=', rec.finger_print_id)],
                                                             limit=1)
                if employee_id:
                    rec.employee_id = employee_id.id
    @api.model
    def create(self, vals):
        if vals.get('finger_print_id'):
            employee_id = self.env['hr.employee'].search([('finger_print_id', '=', vals.get('finger_print_id'))],
                                                         limit=1)
            if employee_id:
                vals['employee_id'] = employee_id.id
        return super(HrAttendance, self).create(vals)