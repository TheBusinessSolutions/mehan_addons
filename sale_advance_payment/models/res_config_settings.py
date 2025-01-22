# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    sale_advance_journal_id = fields.Many2one(
        "account.journal",
        "Journal",
        required=True)


    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res.update(
            sale_advance_journal_id=int(self.env['ir.config_parameter'].sudo().get_param(
                'sale_advance_payment.sale_advance_journal_id')),

        )
        return res

    def set_values(self):
        super(ResConfigSettings, self).set_values()

        param = self.env['ir.config_parameter'].sudo()
        sale_advance_journal_id = self.sale_advance_journal_id and self.sale_advance_journal_id.id or False

        param.set_param('sale_advance_payment.sale_advance_journal_id', sale_advance_journal_id)
