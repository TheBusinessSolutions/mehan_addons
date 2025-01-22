# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    purchase_advance_journal_id = fields.Many2one(
        "account.journal",
        "Journal",
        required=True)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            purchase_advance_journal_id=int(self.env['ir.config_parameter'].sudo().get_param(
                'purchase_advance_payment.purchase_advance_journal_id')),

        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        param = self.env['ir.config_parameter'].sudo()
        purchase_advance_journal_id = self.purchase_advance_journal_id and self.purchase_advance_journal_id.id or False

        param.set_param('purchase_advance_payment.purchase_advance_journal_id', purchase_advance_journal_id)
