# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class EmployeeChecklist(models.Model):
    _name = 'custom.employee.checklist'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    name = fields.Char(string='Checklist')




class EmployeeChecklistDocument(models.Model):
    _name = 'custom.employee.checklist.document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date DESC'

    name = fields.Char(default="/", readonly=True)
    checklist_id = fields.Many2one('custom.employee.checklist', string="Checklist")
    employee_id = fields.Many2one('hr.employee', string='Employee')
    is_attached = fields.Boolean()

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('custom.employee.checklist.document') or 'New'
        result = super(EmployeeChecklistDocument, self).create(vals)
        return result

    @api.onchange('is_attached')
    def get_documents_progress(self):
        for rec in self:
            if rec.is_attached == True:
                rec.employee_id.write({'entry_checklist': [(4, rec.checklist_id.id)]})
            else:
                rec.employee_id.write({'entry_checklist': [(3, rec.checklist_id.id)]})




class EmployeeMasterInherit(models.Model):
    _inherit = 'hr.employee'

    @api.depends('entry_checklist')
    def entry_progress(self):
        for each in self:
            total_len = self.env['custom.employee.checklist'].search_count([])
            entry_len = len(each.entry_checklist)
            if total_len != 0:
                each.entry_progress = (entry_len * 100) / total_len

    entry_progress = fields.Float(compute=entry_progress, string='Entry Progress', store=True, default=0.0,
                                  help="Percentage of Entry Checklists's")

    entry_checklist = fields.Many2many('custom.employee.checklist', 'entry_obj', 'check_hr_rel', 'hr_check_rel',
                                       string='Entry Process')

    entry_document_count = fields.Integer(compute='_document_count', string='# Entry Documents')

    def _document_count(self):
        for each in self:
            entry_document_ids = self.env['custom.employee.checklist.document'].sudo().search([('employee_id', '=', each.id)])
            each.entry_document_count = len(entry_document_ids)

    def entry_document_view(self):
        self.ensure_one()
        domain = [
            ('employee_id', '=', self.id)]
        return {
            'name': _('Documents'),
            'domain': domain,
            'res_model': 'custom.employee.checklist.document',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'tree,form',
            'context': "{'default_employee_id': %s}" % self.id
        }

    def add_checklists_button(self):
        for rec in self:
            checklists = self.env['custom.employee.checklist'].sudo().search([])
            if checklists:
                for check in checklists:
                    exist_document = self.env['custom.employee.checklist.document'].sudo().search([('employee_id', '=', rec.id), ('checklist_id', '=', check.id)])
                    if len(exist_document) > 0:
                        continue
                    else:
                        vals = []
                        vals.append({
                            'checklist_id': check.id,
                            'employee_id': rec.id
                        })
                        if vals:
                            self.env['custom.employee.checklist.document'].sudo().create(vals)


