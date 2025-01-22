from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    zip_id = fields.Many2one(related='partner_id.zip_id',store=True)
    city_id = fields.Many2one(related='partner_id.city_id',store=True)
