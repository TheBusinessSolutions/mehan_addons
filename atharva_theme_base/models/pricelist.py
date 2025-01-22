# -*- coding: utf-8 -*-

from odoo import models, fields

class PriceListExtend(models.Model):
    _inherit = 'product.pricelist.item'
    _description = 'Product Discount Countdown'

    show_timer = fields.Boolean(string='Show Timer', default=False)
    show_offers = fields.Boolean(string='Show Future Offers', default=False)
    offer_msg = fields.Char(string='Offer Message', default="Hurry Up! Limited time offer.", required=True)
    offer_alert_msg = fields.Text(string='Offer Days Left',  default="New offer coming in @ days")
