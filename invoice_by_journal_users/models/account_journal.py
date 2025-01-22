# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    custom_user_ids = fields.Many2many(
        'res.users', 
        string='Allow Access Users',
        copy=True,
    )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env['res.users'].has_group('invoice_by_journal_users.group_limited_acces_journal_user'):
            args += [('custom_user_ids', 'in', self.env.user.ids)]
            return super(AccountJournal, self)._search(args, offset, limit, order, count, access_rights_uid)
        else:
            return super(AccountJournal, self)._search(args, offset, limit, order, count, access_rights_uid)

    def read(self, fields=None, load='_classic_read'):
        journals = super(AccountJournal, self).read(fields=fields, load=load)
        if len(journals) == 1:
            if self.env.user.has_group("invoice_by_journal_users.group_limited_acces_journal_user"):
                journal_restrict_access_config = self.env['account.journal'].sudo().search([('custom_user_ids', 'in', self.env.user.ids)])
                if journal_restrict_access_config:
                    for journal in journals:
                        if journal.get('id') and journal.get('id') not in journal_restrict_access_config.ids:
                            raise AccessError(_("You don't have the access!"))
        return journals

