# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _

class HrLoan(models.Model):
    _inherit = 'hr.loan'

    state = fields.Selection(selection_add=[('departmentapprove', "Department Approval"), ('hrapprove', "HR Manager Approval"), ('waiting_approval_1',)])
    is_department_manager = fields.Boolean(string="Department Manager", compute="_compute_is_department_manager", )


    @api.model
    def create(self, values):
        res = super(HrLoan, self).create(values)
        for rec in res:
            if rec.department_id.manager_id.user_id.partner_id.id:
                msg = _('%(employee)s requests loan', employee=rec.employee_id.name)
                rec.message_post(body=msg, partner_ids=[rec.department_id.manager_id.user_id.partner_id.id])
        return res


    def action_department_approve(self):
        self.write({'state': 'departmentapprove'})
        hr_manager_group = self.env.ref('hr.group_hr_manager')
        partner_ids = [user.partner_id.id for user in hr_manager_group.users]
        if partner_ids:
            self.message_post(body='Department manager approved loan request', partner_ids=partner_ids)

    def action_hr_approve(self):
        self.write({'state': 'hrapprove'})

    @api.depends('department_id')
    def _compute_is_department_manager(self):
        for rec in self:
            rec.is_department_manager = False
            if rec.department_id.manager_id:
                if rec.department_id.manager_id.user_id == self.env.user:
                    rec.is_department_manager = True





