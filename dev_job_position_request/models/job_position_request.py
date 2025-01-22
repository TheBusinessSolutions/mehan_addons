# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd
#    (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

from odoo import models, fields, api
from datetime import datetime


class JobPositionRequest(models.Model):
    _name = "job.position.request"
    _description = "Create new job positions from here"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    
    def make_url(self):
        ir_param = self.env['ir.config_parameter'].sudo()
        base_url = ir_param.get_param('web.base.url')
        menu_id = self.env.ref("dev_job_position_request.menu_job_position_request").id
        action_id = self.env.ref("dev_job_position_request.action_dev_job_position_request").id
        if base_url:
            base_url += '/web#id=%s&cids=1&menu_id=%s&action=%s&model=%s&view_type=form' % (self.id, menu_id, action_id, self._name)
        return base_url

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('job.position.request.sequence') or 'New'
        return super(JobPositionRequest, self).create(vals)

    @api.returns('self')
    def _get_employee(self):
        return self.env['hr.employee'].search([('user_id', '=', self.env.uid)], limit=1) or False

    def submit_to_manager(self):
        self.state = "to approve"
        if not self.env.user.has_group('hr_recruitment.group_hr_recruitment_manager'):
            authorized_group = self.env.ref('hr_recruitment.group_hr_recruitment_manager')
            
            if authorized_group and authorized_group.users:
                authorized_users = authorized_group.users
                email_from = self.env.user and self.env.user.partner_id and self.env.user.partner_id.email or ''
                template = self.env.ref("dev_job_position_request.email_template_job_position_request")
                if template and email_from and authorized_users:
                    template_id = self.env['mail.template'].browse(int(template))
                    if template_id:
                        for user in authorized_users:
                            if user.partner_id and user.partner_id.email:
                                template_id.write({'email_from': email_from})
                                template_id.write({'email_to': user.partner_id.email})
                                template_id.send_mail(self.id, force_send=True)

    def send_job_position_created_email(self, job_id):
        if self.job_id and self.employee_id:
            if self.employee_id.user_id and self.employee_id.user_id.partner_id and self.employee_id.user_id.partner_id.email:
                if self.env.user and self.env.user.partner_id and self.env.user.partner_id.email:
                    template = self.env.ref("dev_job_position_request.template_manger_to_user")
                    if template:
                        template_id = self.env['mail.template'].browse(int(template))
                        if template_id:
                            template_id.write({'email_from': self.env.user.partner_id.email})
                            template_id.write({'email_to': self.employee_id.user_id.partner_id.email})
                            template_id.send_mail(self.id, force_send=True)

    def send_job_position_rejected_email(self):
        if self.employee_id.user_id and self.employee_id.user_id.partner_id and self.employee_id.user_id.partner_id.email:
            if self.env.user and self.env.user.partner_id and self.env.user.partner_id.email:
                template = self.env.ref("dev_job_position_request.email_template_job_position_request_rejected")
                if template:
                    template_id = self.env['mail.template'].browse(int(template))
                    if template_id:
                        template_id.write({'email_from': self.env.user.partner_id.email})
                        template_id.write({'email_to': self.employee_id.user_id.partner_id.email})
                        template_id.send_mail(self.id, force_send=True)

    def approve_request(self):
        job_id = self.env['hr.job'].search([('id', '=', self.job_id.id)])
        if job_id:
            self.state = 'approved'
            job_id.no_of_recruitment += self.expected_new_employees
            if self.employee_id and self.employee_id.user_id:
                if self.env.user.id == self.employee_id.user_id.id:
                    pass
                else:
                    self.send_job_position_created_email(job_id)
            else:
                self.send_job_position_created_email(job_id)

    def reject_request(self):
        self.state = "rejected"
        if self.employee_id and self.employee_id.user_id:
            if self.env.user.id == self.employee_id.user_id.id:
                pass
            else:
                self.send_job_position_rejected_email()
        else:
            self.send_job_position_rejected_email()

    def set_to_new(self):
        self.state = "new"

    def view_job_position(self):
        form_id = self.env.ref("hr.view_hr_job_form").id
        return {'name': 'Job Position',
                'type': 'ir.actions.act_window',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'hr.job',
                'views': [(form_id, 'form')],
                'target': 'current',
                'res_id': self.job_id.id
                }

    # def create_new_job_position(self):
    #     job_id = self.env['hr.job'].search([('id', '=', self.job_id.id)])
    #     if job_id:
    #         self.state = 'job_position_created'
    #         job_id.no_of_recruitment += self.expected_new_employees
    #         if self.employee_id and self.employee_id.user_id:
    #             if self.env.user.id == self.employee_id.user_id.id:
    #                 pass
    #             else:
    #                 self.send_job_position_created_email(job_id)
    #         else:
    #             self.send_job_position_created_email(job_id)

    def job_position_details(self):
        position_details = []
        for line in self:
            position_details.append({'name':str(line.name),
                                     'date':str(line.date),
                                     'employee_id':str(line.employee_id.name),
                                     'expected_new_employees': str(line.expected_new_employees)
                                    })
        return position_details

    name = fields.Char(string="Sequence", copy=False, readonly=1)
    employee_id = fields.Many2one("hr.employee", string="Requested By", default=_get_employee, readonly=1)
    department_id = fields.Many2one("hr.department", string="Department")
    expected_new_employees = fields.Integer(string="Expected New Employees", required=1)
    date = fields.Date(string="Requested On", default=fields.Date.context_today)
    due_date = fields.Date(string="Due Date")
    job_id = fields.Many2one("hr.job", string="Job Position", copy=False)
    company_id = fields.Many2one("res.company", string="Company", default=lambda self: self.env.user.company_id, copy=False)
    description = fields.Text(string="Description")
    state = fields.Selection(selection=[('new', 'New'),
                                        ('to approve', 'To Approve'),
                                        ('approved', 'Approved'),
                                        # ('job_position_created', 'Job Position Created'),
                                        ('rejected', 'Rejected'),
                                        ], default='new', string="State")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
