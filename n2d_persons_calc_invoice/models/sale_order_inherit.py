# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _


class SaleOrder(models.Model):
    _inherit = "sale.order"

    is_party = fields.Boolean("is a Party?")
    dishes_ids = fields.One2many('party.dishes', 'order_id', copy=True)
    delivery_count = fields.Integer(string='Delivery Orders', compute='_compute_picking_ids')

    def action_view_delivery(self):
        self.ensure_one()
        if self.is_party:
            move_ids = []
            for line in self.dishes_ids:
                move = self.env['stock.move'].search([('dish_id', '=', line.id)])
                for pick in move:
                    move_ids.append(pick.picking_id.id)
            action = self.env.ref('stock.action_picking_tree_all').read()[0]

            if len(move_ids) > 1:
                action['domain'] = [('id', 'in', move_ids)]
            elif move_ids:
                action['views'] = [(self.env.ref('stock.view_picking_form').id, 'form')]
                action['res_id'] = move_ids[0]
            return action
        else:
            return super(SaleOrder, self).action_view_delivery()

    @api.depends('picking_ids', 'is_party')
    def _compute_picking_ids(self):
        for order in self:
            if order.is_party:
                move_ids = []
                for line in order.dishes_ids:
                    move = self.env['stock.move'].search([('dish_id', '=', line.id)])
                    for pick in move:
                        if pick.picking_id.id not in move_ids:
                            move_ids.append(pick.picking_id.id)
                order.delivery_count = len(move_ids)
            else:
                order.delivery_count = len(order.picking_ids)

    def _prepare_invoice(self):
        invoice_values = super(SaleOrder, self)._prepare_invoice()
        dishes = []
        for dish in self.dishes_ids:
            dishes.append((0, 0, {
                'product_id': dish.product_id.id,
                'product_uom_qty': dish.product_uom_qty,
                'unit_price': dish.unit_price,
            }))
        invoice_values.update({'is_party': self.is_party, 'dishes_ids': dishes})
        return invoice_values

    def action_confirm(self):
        for rec in self:
            if not rec.is_party:
                super(SaleOrder, self).action_confirm()
            else:
                picking_type_id = self.env['stock.picking.type'].search(
                    [('code', '=', 'outgoing'), ('warehouse_id', '=', rec.warehouse_id.id)], limit=1)
                move_lines = []
                for line in rec.dishes_ids:
                    values = {
                        'name': line.product_id.name,
                        'product_id': line.product_id.id,
                        'product_uom_qty': line.product_uom_qty,
                        'product_uom': line.product_id.uom_id.id,
                        'location_id': picking_type_id.default_location_src_id.id,
                        'location_dest_id': rec.partner_id.property_stock_customer.id,
                        'sale_line_id': rec.order_line[0].id if rec.order_line else False,
                        'warehouse_id': rec.warehouse_id.id or False,
                        'dish_id': line.id
                    }
                    move_lines.append((0, 0, values))

                self.env['stock.picking'].create({
                    'origin': rec.name,
                    'picking_type_id': picking_type_id.id,
                    'partner_id': rec.partner_id.id,
                    'location_id': picking_type_id.default_location_src_id.id,
                    'location_dest_id': rec.partner_id.property_stock_customer.id,
                    'move_lines': move_lines,
                    'move_type': 'one',
                    'sale_id': rec.id,
                    # 'warehouse_id': rec.warehouse_id.id or False,
                })
                rec.state = 'sale'
