# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class PartyDishes(models.Model):
    _name = 'party.dishes'

    product_id = fields.Many2one('product.product', "Product")
    unit_price = fields.Float("Unit Price")
    product_uom_qty = fields.Float("Quantity")
    order_id = fields.Many2one('sale.order', "Order")
    invoice_id = fields.Many2one('account.move', "Invoice")


    @api.onchange('product_id')
    def get_product_price(self):
        for rec in self:
            if rec.product_id:
                rec.unit_price = rec.product_id.lst_price
