# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = "account.move"

    is_party = fields.Boolean("Is a Party?")
    dishes_ids = fields.One2many('party.dishes', 'invoice_id')


class saleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _create_invoice(self, order, so_line, amount):
        invoice = super(saleAdvancePaymentInv, self)._create_invoice(order, so_line, amount)
        invoice.is_party = order.is_party
        dishes = []
        for dish in order.dishes_ids:
            dishes.append((0, 0, {
                'product_id': dish.product_id.id,
                'product_uom_qty': dish.product_uom_qty,
                'unit_price': dish.unit_price,
            }))
        invoice.dishes_ids = dishes

        return invoice
