from odoo import models, fields, api, exceptions,_
from datetime import date, datetime, time, timedelta
from odoo.exceptions import RedirectWarning, UserError, ValidationError


# class acc_move(models.Model):
#
#     _inherit = 'account.move'

class move_lines(models.Model):

    _inherit = 'account.move.line'

    jebal_pay_id = fields.Integer(string="Jebal Payment",index=True)
    jebal_check_id = fields.Integer(string="Jebal Check",index=True)
    jebal_nrom_pay_id = fields.Integer(string="Jebal Check", index=True)
    jebal_con_pay_id = fields.Integer(string="Jebal Check", index=True)
    date_maturity = fields.Date(string='Due date', index=True, required=False,
                                help="This field is used for payable and receivable journal entries. You can put the limit date for the payment of this line.")

    # @api.model
    # def create(self,vals):
    #     res = super(move_lines,self).create(vals)
    #     res.date_maturity = False
    #     return res

    @api.constrains('currency_id', 'account_id')
    def _check_account_currency(self):
        for line in self:
            account_currency = line.account_id.currency_id
            if account_currency and account_currency != line.company_currency_id and account_currency != line.currency_id:
                pass

    @api.model
    def _compute_amount_fields(self, amount, src_currency, company_currency):
        """ Helper function to compute value for fields debit/credit/amount_currency based on an amount and the currencies given in parameter"""
        amount_currency = False
        currency_id = False
        date = self.env.context.get('date') or fields.Date.today()
        company = self.env.context.get('company_id')
        company = self.env['res.company'].browse(company) if company else self.env.user.company_id
        if src_currency and src_currency != company_currency:
            amount_currency = amount
            amount = src_currency._convert(amount, company_currency, company, date)
            currency_id = src_currency.id
        debit = amount > 0 and amount or 0.0
        credit = amount < 0 and -amount or 0.0
        return debit, credit, amount_currency, currency_id


class create_moves(models.Model):
    _name = 'create.moves'

    # @api.multi
    def create_move_lines(self, **kwargs):
        self.accounts_agg(**kwargs)
        self.adjust_move_percentage(**kwargs)
        aml_obj = self.env['account.move.line'].with_context(check_move_validity=False)
        company_currency = self.env['res.users'].search([('id', '=', self._uid)]).company_id.currency_id
        debit, credit, amount_currency, currency_id = aml_obj.with_context(
            date=datetime.today())._compute_amount_fields(kwargs['amount'], kwargs['src_currency'],
                                                         company_currency)

        # debit, credit, amount_currency, currency_id = str(kwargs['amount'])
        move_vals = {
            'name': kwargs['move']['name'],
            'journal_id': kwargs['move']['journal_id'],
            'date': datetime.today(),
            'ref': kwargs['move']['ref'],
            'company_id': kwargs['move']['company_id'],
        }

        move = self.env['account.move'].with_context(check_move_validity=False).create(move_vals)

        for index in kwargs['debit_account']:
            debit_line_vals = {
                'name': kwargs['move_line']['name'],
                'account_id': index['account'],
                'partner_id': kwargs['move_line']['partner_id'],
                'debit': debit,
                'credit': credit,
                'amount_currency': amount_currency,
                'currency_id': currency_id,
            }
            if 'analyitc_id' in index:
                debit_line_vals['analytic_account_id'] = index['analyitc_id']
            if 'jebal_pay_id' in kwargs['move_line']:
                debit_line_vals['jebal_pay_id'] =  kwargs['move_line']['jebal_pay_id']
            if 'jebal_check_id' in  kwargs['move_line']:
                debit_line_vals['jebal_check_id'] = kwargs['move_line']['jebal_check_id']
            if 'jebal_nrom_pay_id' in  kwargs['move_line']:
                debit_line_vals['jebal_nrom_pay_id'] = kwargs['move_line']['jebal_nrom_pay_id']
            if 'jebal_con_pay_id' in  kwargs['move_line']:
                debit_line_vals['jebal_con_pay_id'] = kwargs['move_line']['jebal_con_pay_id']
            debit_line_vals['move_id'] = move.id
            aml_obj.create(debit_line_vals)

        for index in kwargs['credit_account']:
            credit_line_vals = {
                'name': kwargs['move_line']['name'],
                'account_id': index['account'],
                'partner_id': kwargs['move_line']['partner_id'],
                'debit': credit,
                'credit': debit,
                'amount_currency': -1 * amount_currency,
                'currency_id': currency_id,
            }
            if 'analyitc_id' in index:
                credit_line_vals['analytic_account_id'] = index['analyitc_id']
            if 'jebal_pay_id' in kwargs['move_line']:
                credit_line_vals['jebal_pay_id'] =  kwargs['move_line']['jebal_pay_id']
            if 'jebal_check_id' in  kwargs['move_line']:
                credit_line_vals['jebal_check_id'] = kwargs['move_line']['jebal_check_id']
            if 'jebal_nrom_pay_id' in  kwargs['move_line']:
                credit_line_vals['jebal_nrom_pay_id'] = kwargs['move_line']['jebal_nrom_pay_id']
            credit_line_vals['move_id'] = move.id
            aml_obj.create(credit_line_vals)
        # move.post()

    def adjust_move_percentage(self,**kwargs):
        # Debit
        tot_dens = 0.0
        tot_crds = 0.0
        for debs in kwargs['debit_account']:
            tot_dens+=debs['percentage']
        for crds in kwargs['credit_account']:
            tot_crds+=crds['percentage']
        percent = 100.0
        if tot_crds < 99 or tot_crds > 101:
            percent = tot_crds
        for i in range(len(kwargs['debit_account'])):
            kwargs['debit_account'][i]['percentage'] = round(kwargs['debit_account'][i]['percentage'],8)
        for index in kwargs['debit_account']:
            percent -= index['percentage']
        diff = 0.0
        if percent !=0.0:
            diff = percent / len(kwargs['debit_account'])
            for i in range(len(kwargs['debit_account'])):
                kwargs['debit_account'][i]['percentage'] +=diff
        #Credit
        percent = 100.0
        if tot_crds < 99 or tot_crds > 101:
            percent = tot_crds
        for i in range(len(kwargs['credit_account'])):
            kwargs['credit_account'][i]['percentage'] = round(kwargs['credit_account'][i]['percentage'], 8)
        for index in kwargs['credit_account']:
            percent -= index['percentage']
        diff = 0.0
        if percent != 0.0:
            diff = percent / len(kwargs['credit_account'])
            for i in range(len(kwargs['credit_account'])):
                kwargs['credit_account'][i]['percentage'] += diff

    def accounts_agg(self,**kwargs):
        all_crd_accs = {}
        for crd_accs in kwargs['credit_account']:
            if all_crd_accs and crd_accs['account'] in all_crd_accs:
                all_crd_accs[crd_accs['account']] += crd_accs['percentage']
            else:
                all_crd_accs[crd_accs['account']] = crd_accs['percentage']
        credit_account = []
        for acc_key in all_crd_accs:
            credit_account.append({'account': acc_key, 'percentage': all_crd_accs[acc_key]})
        kwargs['credit_account'] = credit_account
        all_crd_accs = {}
        for crd_accs in kwargs['debit_account']:
            if all_crd_accs and crd_accs['account'] in all_crd_accs:
                all_crd_accs[crd_accs['account']] += crd_accs['percentage']
            else:
                all_crd_accs[crd_accs['account']] = crd_accs['percentage']
        debit_account = []
        for acc_key in all_crd_accs:
            debit_account.append({'account': acc_key, 'percentage': all_crd_accs[acc_key]})
        kwargs['debit_account'] = debit_account
