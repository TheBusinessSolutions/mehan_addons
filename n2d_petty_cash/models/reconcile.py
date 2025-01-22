# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ast import literal_eval


class CashInPetty(models.Model):
    _name = 'cash.to.petty'
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', "Employee",ondelete='cascade', domain=[('user_id', '!=', False)],
                                  track_visibility='onchange')
    amount = fields.Float("Amount", track_visibility='onchange')
    account_id = fields.Many2one('account.account', "Account To", domain=lambda self: [
        ('user_type_id.id', '=', self.env.ref('account.data_account_type_liquidity').id)], track_visibility='onchange')
    state = fields.Selection(
        [('draft', "Draft"), ('approved', "Approved"), ('confirmed', "Confirmed"), ('rejected', "Rejected")],
        string="Status", default='draft', track_visibility='onchange')
    move_id = fields.Many2one('account.move', string='Entry', copy=False, track_visibility='onchange')
    entry_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Entry Status', related='move_id.state', store=True)

    # analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account')
    # lab = fields.Char('Label')

    def unlink(self):
        self.action_reject()
        return super(CashInPetty, self).unlink()

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            if rec.move_id and rec.move_id.state == 'posted':
                raise ValidationError("Please Cancel Journal Entry First!")
            rec.state = 'rejected'

    def set_to_draft(self):
        for rec in self:
            if not rec.move_id:
                rec.state = 'draft'
            else:
                raise ValidationError("Move Must Deleted!")

    def action_confirm(self):
        for rec in self:
            params = self.env['ir.config_parameter'].sudo()
            petty_account_id = literal_eval(params.get_param('n2d_petty_cash.petty_cash_account_id', 'False'))
            petty_journal_id = literal_eval(params.get_param('n2d_petty_cash.petty_cash_journal_id', 'False'))
            if not petty_account_id:
                raise ValidationError("PLease Add Petty Cash Account in Accounting Configuration!!")
            if not petty_journal_id:
                raise ValidationError("PLease Add Petty Cash Journal in Accounting Configuration!!")
            if not rec.account_id:
                raise ValidationError("PLease Add Account To!!")
            debit_vals = {
                'debit': rec.amount,
                'credit': 0.0,
                'partner_id': rec.employee_id.user_id.partner_id.id,
                'name': 'Reconcile',
                'account_id': rec.account_id.id,
                # 'analytic_account_id': rec.analytic_account_id.id,

            }
            credit_vals = {
                'debit': 0.0,
                'credit': rec.amount,
                'partner_id': rec.employee_id.user_id.partner_id.id,
                'name': 'Reconcile',
                'account_id': petty_account_id,
                # 'analytic_account_id': rec.analytic_account_id.id,
            }
            vals = {
                'journal_id': petty_journal_id,
                'ref': "Add cash in petty-cash " + str(rec.id),
                'state': 'draft',
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.post()
            rec.move_id = move.id
            rec.state = 'confirmed'
