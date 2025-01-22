# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError, MissingError

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    # @api.depends('move_id.journal_id')
    # def _custom_compute_user_ids(self):
    #     for rec in self:
    #         if rec.move_id.journal_id.custom_user_ids:
    #             rec.custom_user_ids = rec.move_id.journal_id.custom_user_ids

    custom_user_ids = fields.Many2many(
        'res.users', 
        string='Allow Access Users',
        copy=False,
        related='move_id.journal_id.custom_user_ids'
        # compute='_custom_compute_user_ids',
    )

    @api.model
    def _search(self, args, offset=0, limit=None, order=None, count=False, access_rights_uid=None):
        if self.env['res.users'].has_group('invoice_by_journal_users.group_limited_acces_journal_user'):
            args += [('move_id.journal_id.custom_user_ids', 'in', self.env.user.ids)]
            return super(AccountMoveLine, self)._search(args, offset, limit, order, count, access_rights_uid)
        else:
            return super(AccountMoveLine, self)._search(args, offset, limit, order, count, access_rights_uid)

    def read(self, fields=None, load='_classic_read'):
        custom_move_lines = super(AccountMoveLine, self).read(fields=fields, load=load)
        if len(custom_move_lines) == 1:
            if self.env.user.has_group("invoice_by_journal_users.group_limited_acces_journal_user"):
                move_restrict_access_config = self.env['account.move.line'].sudo().search([('custom_user_ids', 'in', self.env.user.ids)])
                if move_restrict_access_config:
                    for move_line in custom_move_lines:
                        if move_line.get('id') and move_line.get('id') not in move_restrict_access_config.ids:
                            raise AccessError(_("You don't have the access!"))
        return custom_move_lines
