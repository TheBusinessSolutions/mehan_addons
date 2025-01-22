# -*- encoding: utf-8 -*-

from odoo import models, fields


class HrEmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    employee_account_id = fields.Many2one('account.account', string="Account")


    def check_petty_cash(self):
        if self.env.user.has_group('n2d_petty_cash.group_petty_cash_approval') or self.env.user.has_group('n2d_petty_cash.group_petty_cash_confirmation'):
            return {
                'name': 'Dashboard',
                'view_type': 'kanban',
                'view_mode': 'kanban',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': ['|', ('in_petty_ids', '!=', False),
                           ('out_petty_ids', '!=', False)],
                'view_id': self.env.ref('n2d_petty_cash.employee_petty_cash_kanban_view').id,

            }
        else:
            return {
                'name': 'Dashboard',
                'view_type': 'kanban',
                'view_mode': 'kanban',
                'res_model': 'hr.employee',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'domain': [('user_id', '=', self.env.user.id),'|',('in_petty_ids', '!=', False),('out_petty_ids', '!=', False)],
                'view_id': self.env.ref('n2d_petty_cash.employee_petty_cash_kanban_view').id,

            }
