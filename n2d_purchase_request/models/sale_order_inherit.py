# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_count = fields.Float(compute="get_purchase_count", string="Purchase")
    purchase_created = fields.Boolean(compute="get_purchase", store=True, string="Has Purchase?")

    @api.depends('purchase_count')
    def get_purchase(self):
        for rec in self:
            rec.purchase_created = True if rec.purchase_count> 0 else False

    def create_purchase_order(self):
        self.ensure_one()
        return {
            'name': _('Create Purchase Order'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'purchase.request',
            'view_id': self.env.ref('n2d_purchase_request.create_purchase_order_wizard').id,
            'type': 'ir.actions.act_window',
            'context': {
                'default_sale_id': self.id,
            },
            'target': 'new',
        }

    def action_open_po_orders(self):
        self.ensure_one()
        purchase_order_obj = self.env['purchase.order'].search([('sale_order_id', '=', self.id)]).ids
        action = self.env.ref('purchase.purchase_form_action').read()[0]
        action['domain'] = [('id', 'in', purchase_order_obj)]
        return action


    def get_purchase_count(self):
        for order in self:
            purchase_order_obj = self.env['purchase.order'].search([('sale_order_id', '=', order.id)]).ids
            order.purchase_count = len(purchase_order_obj)

