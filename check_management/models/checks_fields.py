# -*- coding: utf-8 -*-
from odoo import models, fields, api, exceptions,_
import odoo.addons.decimal_precision as dp
from datetime import datetime
from datetime import timedelta
from odoo.fields import Date as fDate

class check_management(models.Model):

    _name = 'check.management'
    _description = 'Check'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    check_number = fields.Char(string=_("Check Number"),required=True,default="0")
    check_date = fields.Date(string=_("Check Date"),required=True)
    check_bank = fields.Many2one('res.bank', string=_('Check Bank'))
    dep_bank = fields.Many2one('res.bank', string=_('Depoist Bank'))
    amount = fields.Float(string=_('Check Amount'),digits=dp.get_precision('Product Price'))

    amount_reg = fields.Float(string="Check Regular Amount", digits=dp.get_precision('Product Price'))


    open_amount_reg = fields.Float(string="Check Regular Open Amount", digits=dp.get_precision('Product Price'))

    open_amount = fields.Float(string=_('Open Amount'), digits=dp.get_precision('Product Price'),track_visibility='onchange')
    investor_id = fields.Many2one('res.partner',string=_("Partner"))





    type = fields.Selection(string="Type", selection=[('reservation', 'Reservation instalment'),
                                                      ('contracting', 'Contracting instalment'),
                                                      ('regular', 'Regular instalment'),
                                                      ('ser', 'Services instalment'),
                                                      ('garage', 'Garage instalment'),
                                                      ('mod', 'Modification instalment'),
                                                      ], required=True,translate=True,
                            default="regular")
    state = fields.Selection(selection=[('holding','Holding'),('depoisted','Depoisted'),
                                         ('approved','Approved'),('rejected','Rejected')
                                         , ('returned', 'Returned'), ('handed', 'Handed'),
                                        ('debited', 'Debited'),('canceled', 'Canceled'),('cs_return','Customer Returned')]
                             ,translate=True,track_visibility='onchange')

    notes_rece_id = fields.Many2one('account.account')
    under_collect_id  = fields.Many2one('account.account')
    notespayable_id = fields.Many2one('account.account')
    under_collect_jour = fields.Many2one('account.journal')
    check_type = fields.Selection(selection=[('rece','Notes Receivable'),('pay','Notes Payable')])
    check_state = fields.Selection(selection=[('active','Active'),('suspended','Suspended')],default='active')
    check_from_check_man = fields.Boolean(string="Check Managment",default=False)
    #will_collection = fields.Date(string="Maturity Date" , compute = "_compute_days")
    will_collection_user = fields.Date(string="Bank Maturity Date"  ,track_visibility='onchange')

    # @api.multi
    # def _compute_days(self):
    #     d1=datetime.strptime(str(self.check_date),'%Y-%m-%d')
    #     self.will_collection= d1 + timedelta(days=10)



    @api.model
    def create(self,vals):
        if 'amount' in vals:
            vals['open_amount'] = vals['amount']
        return super(check_management,self).create(vals)

    # @api.multi
    def write(self, vals):
        for rec in self:
            if 'amount' in vals:
                rec.open_amount = vals['amount']
        return super(check_management, self).write(vals)


    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,submenu=False):
        res = super(check_management, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,submenu=submenu)
        if 'fields' in res:
            if 'state' in res['fields']:
                if 'menu_sent' in self.env.context:
                    if self.env.context['menu_sent'] in ('handed','debited'):
                        res['fields']['state']['selection'] = [('handed', 'Handed'), ('debited', 'Debited')]
                        if self.env.context['lang'] == 'ar_SY':
                            res['fields']['state']['selection'] = [('handed', 'مسلمة'), ('debited', 'محصلة')]
                    else:
                        res['fields']['state']['selection'] = [('holding', 'Holding'), ('depoisted', 'Depoisted'), ('approved', 'Approved'),
                                                               ('rejected', 'Rejected'), ('returned', 'Returned'),('canceled', 'Canceled')
                                                               ,('cs_return','Customer Returned')]
                        if self.env.context['lang'] == 'ar_SY':
                            res['fields']['state']['selection'] = [('holding', 'قابضة'), ('depoisted', 'مودعة'),
                                                                   ('approved', 'خالصة'),('rejected', 'مرفوضة'), ('returned', 'مرتجعة'),
                                                                   ('canceled', 'ملغله'),('cs_return','مرتجع للعميل')]
        if 'toolbar' in res:
            if 'menu_sent' in self.env.context:
                if self.env.context['menu_sent'] == 'holding':
                    for i in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][i]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][i]
                            break
                    for i in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][i]['name'] == 'Company Return':
                            del res['toolbar']['action'][i]
                            break
                    for i in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][i]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][i]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'depoist':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'approved':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Approve Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'rejected':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'returned':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'handed':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Approve Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'debited':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Approve Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'canceled':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Approve Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
                if self.env.context['menu_sent'] == 'cs_return':
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Approve Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Reject Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Company Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Cancel Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Depoist Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Debit Checks':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Customer Return':
                            del res['toolbar']['action'][j]
                            break
                    for j in range(len(res['toolbar']['action'])):
                        if res['toolbar']['action'][j]['name'] == 'Split-Merge':
                            del res['toolbar']['action'][j]
                            break
        return res
