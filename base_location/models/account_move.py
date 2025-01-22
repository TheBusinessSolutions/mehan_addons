from odoo import models, fields, api, _


class AccountMove(models.Model):
    _inherit = 'account.move'

    zip_id = fields.Many2one(related='partner_id.zip_id', store=True)
    city_id = fields.Many2one(related='partner_id.city_id', store=True)