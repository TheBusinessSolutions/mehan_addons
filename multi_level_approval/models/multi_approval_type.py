# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################

from odoo import api, models, fields, _
import logging

_logger = logging.getLogger(__name__)


class MultiApprovalType(models.Model):
    _name = 'multi.approval.type'
    _description = 'Multi Approval Type'

    name = fields.Char(string='Name', required=True)
    image = fields.Binary(attachment=True)
    active = fields.Boolean(string='Active', default=True, readonly=False)

    line_ids = fields.One2many(
        'multi.approval.type.line', 'type_id', string="Approvers",
        required=True)

    approval_minimum = fields.Integer(
        string='Minimum Approvers', compute='_get_approval_minimum',
        readonly=True)

    document_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ], string="Document", default='Optional')
    contact_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Contact", default='None')
    date_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Date", default='None')
    period_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Period", default='None')
    item_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Item", default='None')
    quantity_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Quantity", default='None')
    amount_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Amount", default='None')
    reference_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Reference", default='None')
    # sign = fields.Selection(
    #     [('no_sign_in', 'No Sign In'),
    #      ('no_sign_out', 'No Sign Out'),
    #      ('no_sign_in_out', 'No Sign In/Out'),
    #      ], string="Attendance status", default='no_sign_in_out')
    payment_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Payment", default='None')
    location_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Location", default='None')
    is_excuse = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Is Excuse", default='False')
    emergency = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Emergency", default='False')
    leave_type = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Leave Type")
    formal_assign = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Formal Assignment", default='False')
    return_from_leave = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Return From Leave", default='False')
    submitted_nb = fields.Integer(
        string="To Review",
        compute="_get_submitted_request")

    cer_name = fields.Many2one('multi.certificate',string='Name', required=True)

    need_certification = fields.Selection(
        [('Yes', 'Yes'),
         ('No', 'No'),
         ], string="Need Certification ?", default='Yes')

    regular_leave = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Regular Leave", default='True')


    def _get_submitted_request(self):
        for r in self:
            r.submitted_nb = self.env['multi.approval'].search_count(
                [('type_id', '=', r.id), ('state', '=', 'Submitted')])

    @api.depends('line_ids')
    def _get_approval_minimum(self):
        for rec in self:
            required_lines = rec.line_ids.filtered(
                lambda l: l.require_opt == 'Required')
            rec.approval_minimum = len(required_lines)

    def create_request(self):
        for rec in self:
            if rec.is_excuse == 'True':
                self.ensure_one()
                view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'hr.leave',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',
                    'domain': [('holidays_status_id.excuse', '=', True)],
                    'context': {
                        'default_source':'excuse',
                        'default_holidays_status_id': False,
                    }
                }
            elif rec.emergency == 'True':
                self.ensure_one()
                view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'hr.leave',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',
                    'domain': [('holidays_status_id.emergency_leave', '=', True)],
                    'context': {
                        'default_source':'emergency_leave',
                        'default_holidays_status_id': False,
                    }
                }
            elif rec.regular_leave == 'True':
                self.ensure_one()
                view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'hr.leave',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',
                    'domain': [('holidays_status_id.source', '=', 'regular_leave')],
                    'context': {
                        'default_source':'regular_leave',
                        'default_holidays_status_id': False,
                    }
                }
            elif rec.formal_assign == 'True':
                self.ensure_one()
                view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'hr.leave',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',
                    'domain': [('holidays_status_id.formal_assignment', '=', True)],
                    'context': {
                        'default_source':'formal_assignment',
                        'default_holidays_status_id': False,
                    }
                }
            elif rec.leave_type == 'True':
                self.ensure_one()
                view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'hr.leave',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',
                    'domain': [('holidays_status_id.excuse', '!=', True)],
                    'context': {
                        'default_source': 'other',
                        'default_holidays_status_id': False,
                    }
                }
            else:
                self.ensure_one()
                view_id = self.env.ref(
                    'multi_level_approval.multi_approval_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'form',
                    'res_model': 'multi.approval',
                    'view_id': view_id and view_id.id or False,
                    'type': 'ir.actions.act_window',

                    'context': {
                        'default_type_id': self.id,
                    }
                }

    def open_submitted_request(self):
        for rec in self:
            if rec.is_excuse == 'True':
                self.ensure_one()
                tree_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_tree_my', False)
                form_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('Submitted Requests'),
                    'view_mode': 'tree,form',
                    'res_model': 'hr.leave',
                    'views': [(tree_view_id.id, 'tree'),(form_view_id.id, 'form')],
                    'type': 'ir.actions.act_window',
                    'domain': [('source', '=', 'excuse')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }
            elif rec.emergency == 'True':
                self.ensure_one()
                tree_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_tree_my', False)
                form_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'tree,form',
                    'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                    'res_model': 'hr.leave',
                    'type': 'ir.actions.act_window',
                    'domain': [('source', '=', 'emergency_leave')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }
            elif rec.regular_leave == 'True':
                self.ensure_one()
                tree_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_tree_my', False)
                form_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'tree,form',
                    'res_model': 'hr.leave',
                    'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                    'type': 'ir.actions.act_window',
                    'domain': [('source', '=', 'regular_leave')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }

            elif rec.formal_assign == 'True':
                self.ensure_one()
                tree_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_tree_my', False)
                form_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'tree,form',
                    'res_model': 'hr.leave',
                    'views': [(tree_view_id.id, 'tree'), (form_view_id.id, 'form')],
                    'type': 'ir.actions.act_window',
                    'domain': [('source', '=', 'formal_assignment')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }
            elif rec.leave_type == 'True':
                self.ensure_one()
                tree_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_tree_my', False)
                form_view_id = self.env.ref(
                    'hr_holidays.hr_leave_view_form', False)
                return {
                    'name': _('New Request'),
                    'view_mode': 'tree,form',
                    'res_model': 'hr.leave',
                    'views': [(tree_view_id.id, 'tree'),(form_view_id.id, 'form')],
                    'type': 'ir.actions.act_window',
                    'domain': [('source', '=', 'other')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }
            else:
                self.ensure_one()
                view_id = self.env.ref(
                    'multi_level_approval.multi_approval_view_form', False)

                return {
                    'name': _('Submitted Requests'),
                    'view_mode': 'tree,form',
                    'res_model': 'multi.approval',
                    'view_id': False,
                    'type': 'ir.actions.act_window',
                    'domain': [('type_id', '=', self.id), ('state', '=', 'Submitted')],
                    'context': {
                        'default_type_id': self.id,
                    }
                }
