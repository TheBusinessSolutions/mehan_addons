from odoo import models, fields, api, _

class account_journal(models.Model):

    _inherit = 'account.journal'
    default_debit_account_id = fields.Many2one('account.account', string='Default Debit Account',
                                               domain="[('deprecated', '=', False), ('company_id', '=', company_id)]",
                                               help="It acts as a default account for debit amount",
                                               ondelete='restrict')

    payment_subtype = fields.Selection([('issue_check',_('Issued Checks')),('rece_check',_('Received Checks'))],string="Payment Subtype")

