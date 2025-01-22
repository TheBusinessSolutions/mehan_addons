# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError

class AccountMove(models.Model):
    _inherit = 'account.move'

    @api.depends('journal_id')
    def _custom_compute_user_ids(self):
        for rec in self:
            rec.custom_user_ids = False
            if rec and rec.journal_id and rec.journal_id.custom_user_ids:
                rec.custom_user_ids = rec.journal_id.custom_user_ids
            else:
                rec.custom_user_ids = False


    custom_user_ids = fields.Many2many(
        'res.users', 
        string='Allow Access Users',
        copy=False,
        compute='_custom_compute_user_ids',
    )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env['res.users'].has_group('invoice_by_journal_users.group_limited_acces_journal_user'):
            args += [('journal_id.custom_user_ids', 'in', self.env.user.ids)]
            return super(AccountMove, self)._search(args, offset, limit, order, count, access_rights_uid)
        else:
            return super(AccountMove, self)._search(args, offset, limit, order, count, access_rights_uid)

    def read(self, fields=None, load='_classic_read'):
        custom_moves = super(AccountMove, self).read(fields=fields, load=load)
        if len(custom_moves) == 1:
            if self.env.user.has_group("invoice_by_journal_users.group_limited_acces_journal_user"):
                move_restrict_access_config = self.env['account.move'].sudo().search([('custom_user_ids', 'in', self.env.user.ids)])
                if move_restrict_access_config:
                    for move in custom_moves:
                        if move.get('id') and move.get('id') not in move_restrict_access_config.ids:
                            raise AccessError(_("You don't have the access!"))
        return custom_moves

