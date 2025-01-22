# -*- coding: utf-8 -*-


from odoo import api, fields, models,_


class PartnerViewInherit(models.TransientModel):
    _inherit = 'account.partner.ledger'

    @api.model
    def view_report(self, option,active_partner_id=None):
        r = self.env['account.partner.ledger'].search([('id', '=', option[0])])
        data = {
                'display_account': r.display_account,
                'model': self,
                'journals': r.journal_ids,
                'accounts': r.account_ids,
                'target_move': r.target_move,
                'partners': r.partner_ids,
                'reconciled': r.reconciled,
                'account_type': r.account_type_ids,
                'partner_tags': r.partner_category_ids,
            }
        if active_partner_id:
            partner_id = self.env['res.partner'].search([('id','=',active_partner_id)])
            data['partners'] = partner_id
        
        if r.date_from:
            data.update({
                'date_from':r.date_from,
            })
        if r.date_to:
            data.update({
                'date_to':r.date_to,
            })

        filters = self.get_filter(option)
        records = self._get_report_values(data)
        currency = self._get_currency()

        return {
            'name': "partner Ledger",
            'type': 'ir.actions.client',
            'tag': 'p_l',
            'filters': filters,
            'report_lines': records['Partners'],
            'debit_total': records['debit_total'],
            'credit_total': records['credit_total'],
            'debit_balance': records['debit_balance'],
            'currency': currency,
        }


class ResPartnerInherit(models.Model):
    _inherit = 'res.partner'


    def open_partner_ledger_smart_view(self):
        
    
        return {
            'name': "Partner Ledger",
            'type': 'ir.actions.client',
            'tag': 'smart_pl',
                }
        
