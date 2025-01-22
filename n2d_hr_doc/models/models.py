# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class HREmployee(models.Model):
    _inherit = 'hr.employee'


    @api.depends('document_ids')
    def entry_progress(self):
        for rec in self:
            count = 0
            for line in rec.document_ids:
                if line.is_attached:
                    count += 1

            total_len = self.env['required.document'].search_count([('is_required', '=', True)])
            entry_len = count
            if total_len != 0:
                rec.entry_progress = (entry_len * 100) / total_len



    entry_progress = fields.Float(compute=entry_progress, string='Document Progress', store=True, default=0.0,
                                  help="Percentage of Entry Checklists's")


    document_ids = fields.One2many(comodel_name="employee.document", inverse_name="document_id", string="Documents")

    @api.model
    def create(self, vals):
        res = super(HREmployee, self).create(vals)
        for rec in res:
            required_docs = self.env['required.document'].search([('is_required', '=', True)])
            for doc in required_docs:
                lines = []
                vals = {
                    'required_document_id': doc.id,
                }

                lines.append((0, 0, vals))

                rec.document_ids = lines
        return res




class RequiredDocument(models.Model):
    _name = 'required.document'
    _description = 'Document Required'

    name = fields.Char()
    is_required = fields.Boolean('Required Document')

    @api.model
    def create(self, vals):
        res = super(RequiredDocument, self).create(vals)
        for rec in res:
            if rec.is_required == True:
                employees = self.env['hr.employee'].search([])
                for employee in employees:
                    lines = []
                    vals = {
                        'required_document_id': rec.id,
                    }

                    lines.append((0, 0, vals))

                    employee.document_ids = lines
        return res


    def write(self, vals):
        result = super(RequiredDocument, self).write(vals)
        for rec in self:
            if rec.is_required == True:
                employees = self.env['hr.employee'].search([])
                for employee in employees:
                    if employee.document_ids:
                        exist_document_list = []
                        for line in employee.document_ids:
                            exist_document_list.append(line.required_document_id.id)
                        if rec.id in exist_document_list:
                            pass
                        else:
                            lines = []
                            vals = {
                                'required_document_id': rec.id,
                            }

                            lines.append((0, 0, vals))

                            employee.document_ids = lines

                    else:
                        lines = []
                        vals = {
                            'required_document_id': rec.id,
                        }

                        lines.append((0, 0, vals))

                        employee.document_ids = lines

        return result



class HrEmployeeRequiredDocument(models.Model):
    _name = 'employee.document'
    _description = 'Employee Document'

    is_attached = fields.Boolean(string="Attached", )
    file = fields.Binary('Attachment')
    file_name = fields.Char('File Name')
    required_document_id = fields.Many2one(comodel_name="required.document", string="Document Required")
    document_id = fields.Many2one(comodel_name="hr.employee", string="Document")



