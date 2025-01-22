# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ast import literal_eval


class CashFromPetty(models.Model):
    _name = 'cash.from.petty'
    _rec_name = 'partner_id'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', "Employee",ondelete='cascade', domain=[('user_id', '!=', False)], track_visibility='onchange')
    partner_id = fields.Many2one('res.partner', "Vendor", track_visibility='onchange')
    amount = fields.Float("Amount", track_visibility='onchange')
    state = fields.Selection(
        [('draft', "Draft"), ('approved', "Approved"), ('confirmed', "Confirmed"), ('rejected', "Rejected")],
        string="Status", default='draft', track_visibility='onchange')
    move_id = fields.Many2one('account.move', string='Entry', copy=False, track_visibility='onchange')
    entry_state = fields.Selection(selection=[
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancel', 'Cancelled'),
    ], string='Entry Status', related='move_id.state', store=True)
    analytic_account_id = fields.Many2one('account.analytic.account',string='Analytic Account', track_visibility='onchange')
    lab = fields.Text('Label', track_visibility='onchange')
    account_id = fields.Many2one("account.account", "Account", track_visibility='onchange')
    batch_id = fields.Many2one('petty.batch', "Batch")
    batch_date = fields.Date('Batch Date')

    # product_id = fields.Many2one('product.product', string='Product')
    # price = fields.Float("Price")
    # quantity = fields.Float("Quantity")
    # discount = fields.Float("Discount")
    # tax_id = fields.Many2many('account.tax', string='VAT')
    # total = fields.Float("Total", compute="_total")
    # description = fields.Char(string='Description')

    def unlink(self):
        self.action_reject()
        return super(CashFromPetty, self).unlink()

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
            employee_account_petty_cash = params.get_param('n2d_petty_cash.employee_account_petty_cash')
            if employee_account_petty_cash == 'True':
                if not rec.employee_id.employee_account_id:
                    raise ValidationError("PLease Add Employee Account!!")
                else:
                    petty_account_id = rec.employee_id.employee_account_id.id

            if not petty_account_id:
                raise ValidationError("PLease Add Petty Cash Account in Accounting Configuration!!")
            if not petty_journal_id:
                raise ValidationError("PLease Add Petty Cash Journal in Accounting Configuration!!")
            if not rec.account_id:
                raise ValidationError("PLease Add Account!!")
            debit_vals = {
                'debit': 0.0,
                'credit': rec.amount,
                'partner_id': rec.employee_id.user_id.partner_id.id,
                'name': rec.lab,
                'account_id': petty_account_id,
            }
            credit_vals = {
                'debit': rec.amount,
                'credit': 0.0,
                'partner_id': rec.partner_id.id,
                'name': rec.lab,
                'account_id': rec.account_id.id,
                'analytic_account_id': rec.analytic_account_id.id,
            }
            vals = {
                'journal_id': petty_journal_id,
                'ref': "Pay from petty cash " + str(rec.id),
                'state': 'draft',
                'date': rec.batch_date,
                'line_ids': [(0, 0, debit_vals), (0, 0, credit_vals)]
            }
            move = self.env['account.move'].create(vals)
            move.post()
            rec.move_id = move.id
            rec.state = 'confirmed'

    # @api.depends('price', 'quantity')
    # @api.onchange('price', 'quantity')
    # def _total(self):
    #     for rec in self:
    #         rec.total = (rec.price * rec.quantity)
