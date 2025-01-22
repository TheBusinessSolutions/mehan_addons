#!/usr/bin/python
# -*- coding: utf-8 -*-

import time
from odoo.exceptions import UserError, ValidationError
# from openerp import models, fields, api, _
# from openerp.exceptions import Warning
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class hr_exit_checklist(models.Model):
    _name = 'hr.exit.checklist'
    _description = 'HR Exit CheckList'
    
    name = fields.Char(string="Name", required=True)
    responsible_user_id = fields.Many2many('res.users', 'user_id', 'check_id', 'user_check_rel', string='Responsible Users', required=True)
    notes = fields.Text(string="Notes")

class hr_exit_checklist_line(models.Model):
    _name = 'hr.exit.employee.checklist'
    _description = 'HR Exit Employee CheckList'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee', required=True)
    checklist_ids = fields.One2many('hr.exit.line', 'employee_exit_id')


    @api.constrains('employee_id')
    def _check_exist_employee(self):
        for rec in self:
            exist_employee = self.env['hr.exit.employee.checklist'].search([('employee_id', '=', rec.employee_id.id)])
            if len(exist_employee) > 1:
                raise ValidationError(_('This employee already exists.'))


class hr_exit_line(models.Model):
    _name = 'hr.exit.line'
    _description = "Exit Lines"
    #_inherit = ['mail.thread', 'ir.needaction_mixin']
    _inherit = ['mail.thread', 'mail.activity.mixin']      #   odoo11
    _rec_name = 'checklist_id'
    _order = 'id desc'
    
    
    checklist_id = fields.Many2one('hr.exit.checklist', string="Checklist", required=True)
    notes = fields.Text(string="Remarks")
    state = fields.Selection([('draft', 'New'),
                                ('confirm', 'To Approve'),
                                ('approved', 'Approved'),
                                ('reject', 'Rejected'),
                                ('cancel', 'Cancelled')], string='State', default='draft', track_visibility='onchange')
    exit_id = fields.Many2one('hr.exit')
    employee_exit_id = fields.Many2one('hr.exit.employee.checklist')
    responsible_user_id = fields.Many2many('res.users', 'user_id', 'check_id', 'user_check_rel', string='Responsible Users', related='checklist_id.responsible_user_id')
    employee_id = fields.Many2one('hr.employee', string='Employee', related='employee_exit_id.employee_id')

    # @api.multi #odoo13
    def checklist_confirm(self):
        self.state = 'confirm'
    
    # @api.multi #odoo13
    def checklist_approved(self):
        self.state = 'approved'
        hr_manager_group = self.env.ref('hr.group_hr_manager')
        user_ids = [user.id for user in hr_manager_group.users]
        for hr in user_ids:
            checklist_responsible_activity = self.env['mail.activity'].sudo().create({
                'res_model_id': self.env['ir.model']._get('hr.exit').id,
                'res_id': self.exit_id.id,
                'user_id': hr,
                'summary': 'Checklist responsible has approved exit checklist',
            })
    
    # @api.multi #odoo13
    def checklist_cancel(self):
        self.state = 'cancel'
    
    # @api.multi #odoo13
    def checklist_reject(self):
        self.state = 'reject'
        
class hr_exit(models.Model):
    _name = 'hr.exit'
    _description = "Exit"
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id desc'

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id)
    employee_id = fields.Many2one('hr.employee', required=True, string="Employee")
    request_date = fields.Date('Request Date', readonly='1', default=fields.Date.context_today)
    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user, states={'a_draft':[('readonly', False)]}, readonly=True)
    confirm_date = fields.Date(string='Confirm Date(Employee)', readonly=True, copy=False)
    dept_approved_date = fields.Date(string='Approved Date(Department Manager)', readonly=True, copy=False)
    validate_date = fields.Date(string='Approved Date(HR Manager)', readonly=True, copy=False)
    general_validate_date = fields.Date(string='Approved Date(General Manager)', readonly=True, copy=False)
    
    confirm_by_id = fields.Many2one('res.users', string='Confirm By', readonly=True, copy=False)
    dept_manager_by_id = fields.Many2one('res.users', string='Approved By Department Manager', readonly=True, copy=False)
    hr_manager_by_id = fields.Many2one('res.users', string='Approved By HR Manager', readonly=True, copy=False)
    gen_man_by_id = fields.Many2one('res.users', string='Approved By General Manager', readonly=True, copy=False)
    reason_for_leaving = fields.Char(string='Reason For Leaving',required=True, copy=False, readonly=True)
    last_work_date = fields.Date(string='Last Day of Work')
    survey = fields.Many2one('survey.survey', string="Interview", readonly=True)
    # response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null", oldname="response")
    response_id = fields.Many2one('survey.user_input', "Response", ondelete="set null")
    partner_id = fields.Many2one('res.partner', "Contact", readonly=True)
    
    
    state = fields.Selection(selection=[
                        ('a_draft', 'Draft'), \
                        ('b_confirm', 'Confirmed'), \
                        ('c_approved_dept_manager', 'Approved by Dept Manager'),\
                        ('d_approved_hr_manager', 'Approved by HR Manager'),\
                        ('e_approved_general_manager', 'Approved by General Manager'),\
                        ('f_done', 'Done'),\
                        ('cancel', 'Cancel'),\
                        ('reject', 'Rejected')],string='State', \
                        readonly=True, help='', default='a_draft', \
                        track_visibility='onchange')
    notes = fields.Text(string='Notes')
    manager_id = fields.Many2one('hr.employee', 'Department Manager', related='employee_id.parent_id', readonly=True, store=True,help='This area is automatically filled by the user who will confirm the exit', copy=False)
    department_id = fields.Many2one(
         related='employee_id.department_id', \
                        string='Department', type='many2one', relation='hr.department', \
                        readonly=True, store=True)
    job_id = fields.Many2one(
        related='employee_id.job_id', \
                        string='Job Title', type='many2one', relation='hr.department', \
                        readonly=True, store=True)
    checklist_ids = fields.One2many('hr.exit.line', 'exit_id', string="Checklist")
    contract_id = fields.Many2one('hr.contract', string='Contract', readonly=False)
    contract_ids = fields.Many2many('hr.contract','hr_contract_contract_tag')
    is_department_manager = fields.Boolean(compute="_compute_is_department_manager")

    @api.model
    def create(self, vals):
        res = super(hr_exit, self).create(vals)
        for rec in res:
            exist_exit = self.env['hr.exit'].search([('employee_id', '=', rec.employee_id.id), ('state', '!=', ['cancel', 'reject'])])
            if len(exist_exit) > 1:
               raise UserError(_('The employee already has exit request.'))
            return res

    def unlink(self):
        for rec in self:
            if rec.checklist_ids:
                for line in rec.checklist_ids:
                    line.state = 'draft'
        return super(hr_exit, self).unlink()


    @api.onchange('employee_id')
    def get_employee_domain(self):
        if self.env.user.has_group('actions_management.actions_group_department_manager'):
            domain = [('parent_id.user_id', '=', self.env.user.id)]
            return {'domain': {'employee_id': domain}}

        if not self.env.user.has_group('actions_management.actions_group_department_manager') and not self.env.user.has_group('actions_management.actions_group_administration_manager'):
            domain = [('id', '=', self.env.user.employee_id.id)]
            return {'domain': {'employee_id': domain}}

    @api.depends('manager_id')
    def _compute_is_department_manager(self):
        for rec in self:
            rec.is_department_manager = False
            if rec.manager_id:
                if rec.manager_id.user_id == self.env.user:
                    rec.is_department_manager = True

    
    # @api.multi #odoo13
    def action_makeMeeting(self):
        """ This opens Meeting's calendar view to schedule meeting on current applicant
            @return: Dictionary value for created Meeting view
        """
#         self.ensure_one()
#         partners = self.partner_id | self.user_id.partner_id | self.department_id.manager_id.user_id.partner_id
        
#         category = self.env.ref('hr_recruitment.categ_meet_interview')

        res = self.env['ir.actions.act_window']._for_xml_id('calendar.action_calendar_event')


#         res['context'] = {
#             'search_default_partner_ids': self.partner_id.name,
#             'default_partner_ids': partners.ids,
#             'default_user_id': self.env.uid,
#             'default_name': self.name,
#             'default_categ_ids': category and [category.id] or False,
#         }
        return res
    
    # @api.multi #odoo13
    def action_start_survey(self):
        self.ensure_one()
        # create a response and link it to this applicant
        if not self.response_id:
            response = self.env['survey.user_input'].create({'survey_id': self.survey.id, 'partner_id': self.partner_id.id})
            self.response_id = response.id
        else:
            response = self.response_id
        # grab the token of the response and start surveying
        # return self.survey.with_context(survey_token=response.token).action_start_survey()
        return self.survey.with_context(survey_token=response).action_start_survey()

    # @api.multi #odoo13
    def action_print_survey(self):
        """ If response is available then print this response otherwise print survey form (print template of the survey) """
        self.ensure_one()
        if not self.response_id:
            return self.survey.action_print_survey()
        else:
            response = self.response_id
            return self.survey.with_context(survey_token=response.token).action_print_survey()


    # @api.one #odoo13
    def get_contract_latest(self, employee, date_from, date_to):
        """
        @param employee: browse record of employee
        @param date_from: date field
        @param date_to: date field
        @return: returns the ids of all the contracts for the given employee that need to be considered for the given dates
        """
        contract_obj = self.env['hr.contract']
        clause = []
        #a contract is valid if it ends between the given dates
        clause_1 = ['&',('date_end', '<=', date_to),('date_end','>=', date_from)]
        #OR if it starts between the given dates
        clause_2 = ['&',('date_start', '<=', date_to),('date_start','>=', date_from)]
        #OR if it starts before the date_from and finish after the date_end (or never finish)
        clause_3 = ['&',('date_start','<=', date_from),'|',('date_end', '=', False),('date_end','>=', date_to)]
        clause_final =  [('employee_id', '=', employee.id),'|','|'] + clause_1 + clause_2 + clause_3
        contract_ids = contract_obj.search(clause_final,limit=1)
        return contract_ids
    
    @api.onchange('employee_id', 'state')
    def get_contract(self):
        contract_obj = self.env['hr.contract']
#        if not self.employee_id.address_home_id:
#            raise UserError(_('The employee must have a home address.'))
        self.partner_id = self.sudo().employee_id.address_home_id.id
        all_contract_ids = contract_obj.search([('employee_id', '=', self.employee_id.id)])
        contract_ids = self.get_contract_latest(self.employee_id, self.request_date, self.request_date)
        if contract_ids:
            self.contract_id = contract_ids[0].id
            self.contract_ids = all_contract_ids.ids

    # @api.multi #odoo13
    def exit_approved_by_department(self):
        obj_emp = self.env['hr.employee']
        self.state = 'b_confirm'
        self.dept_approved_date = time.strftime('%Y-%m-%d')

    # @api.multi #odoo13
    def request_set(self):
        self.state = 'a_draft'
    
    # @api.multi #odoo13
    def exit_cancel(self):
        self.state = 'cancel'
        if self.checklist_ids:
            for line in self.checklist_ids:
                line.state = 'draft'

    # @api.multi #odoo13
    def get_confirm(self):
        for rec in self:
            rec.state = 'b_confirm'
            rec.confirm_date = time.strftime('%Y-%m-%d')
            rec.confirm_by_id = self.env.user.id
            dep_manager = rec.sudo().manager_id.user_id.id
            employee = rec.sudo().employee_id.name
            dep_manager_activity = self.env['mail.activity'].sudo().create({
                'res_model_id': self.env['ir.model']._get('hr.exit').id,
                'res_id': rec.id,
                'user_id': dep_manager,
                'summary': employee + 'has confirmed his exit request',
            })

        
    # @api.multi #odoo13
    def get_apprv_dept_manager(self):
        for rec in self:
            rec.checklist_ids = False
            employee_checklists = self.env['hr.exit.employee.checklist'].search(
                [('employee_id', '=', rec.employee_id.id)]).checklist_ids
            if employee_checklists:
                rec.checklist_ids = employee_checklists
        self.state = 'c_approved_dept_manager'
        self.dept_approved_date = time.strftime('%Y-%m-%d')
        self.dept_manager_by_id = self.env.user.id
        for line in self.checklist_ids:
            for u in line.responsible_user_id:
                checklist_responsible_activity = self.env['mail.activity'].sudo().create({
                    'res_model_id': self.env['ir.model']._get('hr.exit.line').id,
                    'res_id': line.id,
                    'user_id': u.id,
                    'summary': self.sudo().employee_id.name + 'submits a resignation request and need to review retrieval of assets',
                })
        
    # @api.multi #odoo13
    def get_apprv_hr_manager(self):
        self.state = 'd_approved_hr_manager'
        self.validate_date = time.strftime('%Y-%m-%d')
        self.hr_manager_by_id = self.env.user.id
        for record in self.checklist_ids:
            if not record.state in ['approved']:
                raise UserError(_('You can not approved this request since there are some checklist to be approved by respected department'))
        gen_manager_group = self.env.ref('actions_management.actions_group_administration_manager')
        user_ids = [user.id for user in gen_manager_group.users]
        for hr in user_ids:
            checklist_responsible_activity = self.env['mail.activity'].create({
                'res_model_id': self.env['ir.model']._get('hr.exit').id,
                'res_id': self.id,
                'user_id': hr,
                'summary': 'Hr manager has approved resignation request for ' + self.sudo().employee_id.name,
            })

        
    # @api.multi #odoo13
    def get_apprv_general_manager(self):
        self.state = 'e_approved_general_manager'
        self.general_validate_date = time.strftime('%Y-%m-%d')
        self.gen_man_by_id = self.env.user.id
        
    # @api.multi #odoo13
    def get_done(self):
        self.state = 'f_done'

    
    # @api.multi #odoo13
    def get_reject(self):
        self.state = 'reject'
        if self.checklist_ids:
            for line in self.checklist_ids:
                line.state = 'draft'
        
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
