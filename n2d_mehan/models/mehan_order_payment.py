# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _
from odoo.exceptions import ValidationError
from datetime import timedelta, date
import dateutil.relativedelta
from dateutil.relativedelta import relativedelta


class MehanOrderPayment(models.Model):
    _name = 'mehan.order.payment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'mehan.order.payment'
    _order = 'create_date DESC'

    name = fields.Char('Order No.', readonly=True, required=True, copy=False, default='New', tracking=True)
    deceased_id = fields.Many2one('deceased.info', string='Name', tracking=True)
    serial = fields.Char('Serial')
    payment_Beneficiaries_ids = fields.One2many('death.beneficiaries.lines', 'order_id',
                                                String='Payment Beneficiaries Lines', tracking=True)
    pension_payment = fields.Binary(related='deceased_id.pension_payment')
    member_type = fields.Selection([
        ('injured', 'Injured'),
        ('dead', 'Dead')
    ], related='deceased_id.member_type')

    payment_amount = fields.Float(string="Payment Amount", related='deceased_id.payment_amount')
    expense_type_id = fields.Many2one('mehan.expense', related='deceased_id.expense_type_id')
    beneficiaries_no = fields.Integer('Beneficiaries Number', compute='_get_num')
    order_compensation_percentage = fields.Float(string="Compensation Percentage", digits=(12, 3))
    company_id = fields.Many2one(
        'res.company', string='Company', change_default=True,
        default=lambda self: self.env.company,
        required=False)
    national_id = fields.Char(related='deceased_id.national_id')

    @api.model
    def create(self, vals):
        vals['name'] = self.env['ir.sequence'].next_by_code('op.sequence') or 'New'
        result = super(MehanOrderPayment, self).create(vals)
        return result

    @api.onchange('deceased_id')
    def _get_beneficiaries_lines(self):
        for rec in self:
            if rec.member_type == 'dead':
                lines = rec.deceased_id.death_Beneficiaries_ids.filtered(lambda l: l.state == 'done')
                for line in lines:
                    if not line.order_id:
                        rec.payment_Beneficiaries_ids += line

            order_compensation_percentage = 0.0
            for line in rec.payment_Beneficiaries_ids:
                order_compensation_percentage += line.compensation_percentage

            rec.order_compensation_percentage = order_compensation_percentage

    @api.depends('payment_Beneficiaries_ids')
    def _get_num(self):
        for rec in self:
            rec.beneficiaries_no = len(rec.payment_Beneficiaries_ids)
