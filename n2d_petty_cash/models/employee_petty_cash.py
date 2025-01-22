from odoo import _, api, fields, models
from odoo.exceptions import ValidationError




class Employee(models.Model):
    _inherit = 'hr.employee'


    petty_cash_total = fields.Float("Total amount", compute='_get_totals')
    last_add_cash = fields.Float("Last add cash", compute='_get_totals')
    cash_expense = fields.Float("Cash expense", compute='_get_totals')
    cash_balance = fields.Float("Balance", compute='_get_totals')
    reconcile_amount = fields.Float("Reconcile", compute='_get_totals')
    in_petty_ids = fields.One2many('cash.in.petty', 'employee_id')
    out_petty_ids = fields.One2many('cash.from.petty', 'employee_id')

    def _get_totals(self):
        for rec in self:
            in_petty = self.env['cash.in.petty'].search([('employee_id', '=', rec.id),('state', '=', 'confirmed'),('entry_state', '!=', 'cancel')], order="create_date desc")
            out_petty = self.env['cash.from.petty'].search([('employee_id', '=', rec.id),('state', '=', 'confirmed'),('entry_state', '!=', 'cancel')])
            reconcile_petty = self.env['cash.to.petty'].search([('employee_id', '=', rec.id),('state', '=', 'confirmed'),('entry_state', '!=', 'cancel')])
            if in_petty:
                rec.last_add_cash = in_petty[0].amount
            else:
                rec.last_add_cash = 0.0
            rec.petty_cash_total = sum([p.amount for p in in_petty])
            rec.cash_expense = sum([p.amount for p in out_petty])
            rec.reconcile_amount = sum([p.amount for p in reconcile_petty])
            rec.cash_balance = rec.petty_cash_total - rec.cash_expense - rec.reconcile_amount

    def action_petty_cash_added(self):
        return {
            'name': 'Added petty cash',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cash.in.petty',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('employee_id', '=', self.id)],
        }

    def action_petty_reconcile(self):
        return {
            'name': 'Reconcile',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'cash.to.petty',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('employee_id', '=', self.id)],
        }

    def action_pay_from_petty(self):
        return {
            'name': 'Purchased from petty cash',
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'petty.batch',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('employee_id', '=', self.id)],

        }


    def action_get_last_cash(self):
        for rec in self:
            last_id = self.env['cash.in.petty'].search([('employee_id', '=', rec.id),('state', '=', 'confirmed'),('entry_state', '!=', 'cancel')])[-1].id
            return {
                'name': 'Last added petty cash',
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'cash.in.petty',
                'type': 'ir.actions.act_window',
                'target': 'current',
                'res_id': last_id,

            }

    def action_get_balance(self):
        pass


    def get_employee_petty_cash(self):
        kanban_view_id = self.env.ref("n2d_petty_cash.employee_petty_cash_kanban_view").id

        return {
            'type': 'ir.actions.act_window',
            'name': 'Dashboard',
            'view_type': 'kanban',
            'view_mode': 'kanban',
            'res_model': 'hr.employee',
            'domain': [('id', '=', self.id)],
            'views': [(kanban_view_id, 'kanban')],
            'target': 'current',
        }
