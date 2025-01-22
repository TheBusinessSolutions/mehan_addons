# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################

from odoo import api, models, fields, _
from odoo.exceptions import Warning
import logging

_logger = logging.getLogger(__name__)


class MultiApproval(models.Model):
    _name = 'multi.approval'
    _inherit = ['mail.thread']
    _description = 'Multi Aproval'
    _rec_name = 'user_id'



    user_id = fields.Many2one(
        string='Request by', comodel_name="res.users",
        required=True, default=lambda self: self.env.uid)

    user_id_assign = fields.Many2one(
        string='Assign To Me', comodel_name="res.users")

    priority = fields.Selection(
        [('0', 'Normal'),
         ('1', 'Medium'),
         ('2', 'High'),
         ('3', 'Very High')], string='Priority', default='0')
    request_date = fields.Datetime(
        string='Request Date', default=fields.Datetime.now)
    type_id = fields.Many2one(
        string="Type", comodel_name="multi.approval.type", required=True)
    description = fields.Html('Description')
    state = fields.Selection(
        [('Draft', 'Draft'),
         ('Submitted', 'Submitted'),
         ('Approved', 'Approved'),
         ('Refused', 'Refused'),
         ('Cancel', 'Cancel')], default='Draft', tracking=True)

    document_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ], string="Document opt", default='Optional',
        readonly=True, related='type_id.document_opt')
    attachment_ids = fields.Many2many('ir.attachment', string='Documents')

    contact_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Contact opt", default='None',
        readonly=True, related='type_id.contact_opt')
    contact_id = fields.Many2one('res.partner', string='Contact')

    date_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Date opt", default='None',
        readonly=True, related='type_id.date_opt')

    period_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Period opt", default='None',
        readonly=True, related='type_id.period_opt')
    date_start = fields.Date('Start Date')
    date_end = fields.Date('End Date')

    item_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Item opt", default='None',
        readonly=True, related='type_id.item_opt')
    item_id = fields.Many2one('product.product', string='Item')

    quantity_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Quantity opt", default='None',
        readonly=True, related='type_id.quantity_opt')
    quantity = fields.Float('Quantity')

    amount_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Amount opt", default='None',
        readonly=True, related='type_id.amount_opt')
    amount = fields.Float('Amount')

    payment_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Payment opt", default='None',
        readonly=True, related='type_id.payment_opt')
    payment = fields.Float('Payment')

    reference_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Reference opt", default='None',
        readonly=True, related='type_id.reference_opt')
    reference = fields.Char('Reference')

    location_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ('None', 'None'),
         ], string="Location opt", default='None',
        readonly=True, related='type_id.location_opt')
    location = fields.Char('Location')
    line_ids = fields.One2many('multi.approval.line', 'approval_id',
                               string="Lines")
    line_id = fields.Many2one('multi.approval.line', string="Line", copy=False)
    deadline = fields.Date(string='Deadline', related='line_id.deadline')
    pic_id = fields.Many2one(
        'res.users', string='Approver', related='line_id.user_id')
    is_pic = fields.Boolean(compute='_check_pic')
    follower = fields.Text('Followers', default='[]', copy=False)

    # copy the idea of hr_expense
    attachment_number = fields.Integer(
        'Number of Attachments', compute='_compute_attachment_number')

    line_cer_ids = fields.One2many(
        'multi.certificate.type.line', 'type_id', string="Certificate",
        required=True)
    certificate_minimum = fields.Integer(
        string='Minimum Certificate', compute='_get_certificate_minimum',
        readonly=True)
    need_certification = fields.Selection(
        [('Yes', 'Yes'),
         ('No', 'No'),
         ], string="Need Certification ?", related='type_id.need_certification')

    check_assign = fields.Boolean(string='Check Assign', default=False, compute='_get_approvers_status')

    date = fields.Date('Date')
    leave_date = fields.Date('Leave Date')
    actual_date = fields.Date('Actual Date')
    period = fields.Integer(string="Period", compute="_duration")
    reason = fields.Char(string='Reason')

    return_from_leave_req = fields.Selection(
        [('True', 'True'),
         ('False', 'False'),
         ], string="Return From Leave", default='False', related='type_id.return_from_leave')

    @api.onchange('leave_date', 'actual_date')
    def _duration(self):
        for rec in self:
            if rec.leave_date and rec.actual_date:
                rec.period = (rec.actual_date - rec.leave_date).days
            else:
                rec.period = 0

    @api.depends('line_cer_ids')
    def _get_certificate_minimum(self):
        for rec in self:
            rec.certificate_minimum = len(rec.line_cer_ids)

    def assign_by(self):
        for rec in self:
            rec.user_id_assign = self.env.uid

    def _get_approvers_status(self):
        for rec in self:
            if rec.line_ids:
                get_value = rec.line_ids[-1]
                if get_value and get_value.state == 'Waiting for Approval':
                    rec.check_assign = True
                else:
                    rec.check_assign = False
            else:
                rec.check_assign = False

    def _check_pic(self):
        for r in self:
            is_pic = False
            if r.pic_id.id == self.env.uid:
                is_pic = True
            elif r.line_id.group_id and self.env.user in r.line_id.group_id.users:
                is_pic = True
            elif r.line_id.head_approve:
                employee_id = self.env['hr.employee'].search([('user_id', '=', r.user_id.id)], limit=1)
                print('r.line_id.head_approve', r.line_id.head_approve)
                print('employee_id', employee_id)
                print(' employee_id.parent_id.user_id.id',  employee_id.parent_id.user_id.id)
                print(' self.env.uid',  self.env.uid)
                if r.line_id.head_approve == 'direct_manager' and employee_id and employee_id.parent_id and employee_id.parent_id.user_id.id == self.env.uid:
                    is_pic = True
                if r.line_id.head_approve == 'department_manager' and employee_id and employee_id.department_id and employee_id.department_id.manager_id and employee_id.department_id.manager_id.user_id and employee_id.department_id.manager_id.user_id.id == self.env.uid:
                    is_pic = True
            r.is_pic = is_pic

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', 'multi.approval'), ('res_id', 'in', self.ids)],
            ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count'])
                          for data in attachment_data)
        for r in self:
            r.attachment_number = attachment.get(r.id, 0)

    def action_cancel(self):
        recs = self.filtered(lambda x: x.state == 'Draft')
        recs.write({'state': 'Cancel'})

    def action_submit(self):
        recs = self.filtered(lambda x: x.state == 'Draft')
        for r in recs:
            # Check if document is required
            if r.document_opt == 'Required' and r.attachment_number < 1:
                raise Warning(_('Document is required !'))
            if not r.type_id.line_ids:
                raise Warning(_(
                    'There is no approver of the type "{}" !'.format(
                        r.type_id.name)))
            r.state = 'Submitted'
        recs._create_approval_lines()

    @api.model
    def get_follow_key(self, user_id=None):
        if not user_id:
            user_id = self.env.uid
        k = '[res.users:{}]'.format(user_id)
        return k

    def update_follower(self, user_id):
        self.ensure_one()
        k = self.get_follow_key(user_id)
        follower = self.follower
        if k not in follower:
            self.follower = follower + k

    # 13.0.1.1
    def set_approved(self):
        self.ensure_one()
        self.state = 'Approved'

    def set_refused(self, reason=''):
        self.ensure_one()
        self.state = 'Refused'

    def action_approve(self):
        ret_act = None
        recs = self.filtered(lambda x: x.state == 'Submitted')
        for rec in recs:
            if not rec.is_pic:
                msg = _('{} do not have the authority to approve this request !'.format(rec.env.user.name))
                self.sudo().message_post(body=msg)
                return False
            line = rec.line_id
            if not line or line.state != 'Waiting for Approval':
                # Something goes wrong!
                self.message_post(body=_('Something goes wrong!'))
                return False

            # Update follower
            rec.update_follower(self.env.uid)

            # check if this line is required
            other_lines = rec.line_ids.filtered(
                lambda x: x.sequence >= line.sequence and x.state == 'Draft')
            if not other_lines:
                ret_act = rec.set_approved()
            else:
                next_line = other_lines.sorted('sequence')[0]
                next_line.write({
                    'state': 'Waiting for Approval',
                })
                rec.line_id = next_line
            line.set_approved()
            msg = _('I approved')
            rec.message_post(body=msg)
        if ret_act:
            return ret_act

    def action_refuse(self, reason=''):
        ret_act = None
        recs = self.filtered(lambda x: x.state == 'Submitted')
        for rec in recs:
            if not rec.is_pic:
                msg = _('{} do not have the authority to approve this request !'.format(rec.env.user.name))
                self.sudo().message_post(body=msg)
                return False
            line = rec.line_id
            if not line or line.state != 'Waiting for Approval':
                # Something goes wrong!
                self.message_post(body=_('Something goes wrong!'))
                return False

            # Update follower
            rec.update_follower(self.env.uid)

            # check if this line is required
            if line.require_opt == 'Required':
                ret_act = rec.set_refused(reason)
                draft_lines = rec.line_ids.filtered(lambda x: x.state == 'Draft')
                if draft_lines:
                    draft_lines.state = 'Cancel'
            else:  # optional
                other_lines = rec.line_ids.filtered(
                    lambda x: x.sequence >= line.sequence and x.state == 'Draft')
                if not other_lines:
                    ret_act = rec.set_refused(reason)
                else:
                    next_line = other_lines.sorted('sequence')[0]
                    next_line.state = 'Waiting for Approval'
                    rec.line_id = next_line
            line.set_refused(reason)
            msg = _('I refused due to this reason: {}'.format(reason))
            rec.message_post(body=msg)
        if ret_act:
            return ret_act

    def _create_approval_lines(self):
        ApprovalLine = self.env['multi.approval.line']
        for r in self:
            lines = r.type_id.line_ids.sorted('sequence')
            last_seq = 0
            for l in lines:
                line_seq = l.sequence
                if not line_seq or line_seq <= last_seq:
                    line_seq = last_seq + 1
                last_seq = line_seq
                vals = {
                    'name': l.name,
                    'user_id': l.get_user(),
                    'sequence': line_seq,
                    'require_opt': l.require_opt,
                    'approval_id': r.id,
                    'head_approve': l.head_approve,
                    'group_id': l.group_id.id or False,
                }
                if l == lines[0]:
                    vals.update({'state': 'Waiting for Approval'})
                approval = ApprovalLine.create(vals)
                if l == lines[0]:
                    r.line_id = approval
