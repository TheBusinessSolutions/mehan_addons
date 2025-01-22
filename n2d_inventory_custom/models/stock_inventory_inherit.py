# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.float_utils import float_compare, float_round, float_is_zero
from odoo.exceptions import ValidationError
import logging
_logger = logging.getLogger(__name__)

# class StockMoveLine(models.Model):
#     _inherit = 'stock.move.line'
#
#     date = fields.Datetime('Date', related='move_id.date', required=True)
#
#     def _action_done(self):
#         """ This method is called during a move's `action_done`. It'll actually move a quant from
#         the source location to the destination location, and unreserve if needed in the source
#         location.
#
#         This method is intended to be called on all the move lines of a move. This method is not
#         intended to be called when editing a `done` move (that's what the override of `write` here
#         is done.
#         """
#
#         # First, we loop over all the move lines to do a preliminary check: `qty_done` should not
#         # be negative and, according to the presence of a picking type or a linked inventory
#         # adjustment, enforce some rules on the `lot_id` field. If `qty_done` is null, we unlink
#         # the line. It is mandatory in order to free the reservation and correctly apply
#         # `action_done` on the next move lines.
#         ml_to_delete = self.env['stock.move.line']
#         for ml in self:
#             # Check here if `ml.qty_done` respects the rounding of `ml.product_uom_id`.
#             uom_qty = float_round(ml.qty_done, precision_rounding=ml.product_uom_id.rounding, rounding_method='HALF-UP')
#             precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#             qty_done = float_round(ml.qty_done, precision_digits=precision_digits, rounding_method='HALF-UP')
#             if float_compare(uom_qty, qty_done, precision_digits=precision_digits) != 0:
#                 raise UserError(_('The quantity done for the product "%s" doesn\'t respect the rounding precision \
#                                   defined on the unit of measure "%s". Please change the quantity done or the \
#                                   rounding precision of your unit of measure.') % (
#                 ml.product_id.display_name, ml.product_uom_id.name))
#
#             qty_done_float_compared = float_compare(ml.qty_done, 0, precision_rounding=ml.product_uom_id.rounding)
#             if qty_done_float_compared > 0:
#                 if ml.product_id.tracking != 'none':
#                     picking_type_id = ml.move_id.picking_type_id
#                     if picking_type_id:
#                         if picking_type_id.use_create_lots:
#                             # If a picking type is linked, we may have to create a production lot on
#                             # the fly before assigning it to the move line if the user checked both
#                             # `use_create_lots` and `use_existing_lots`.
#                             if ml.lot_name and not ml.lot_id:
#                                 lot = self.env['stock.production.lot'].create(
#                                     {'name': ml.lot_name, 'product_id': ml.product_id.id}
#                                 )
#                                 ml.write({'lot_id': lot.id})
#                         elif not picking_type_id.use_create_lots and not picking_type_id.use_existing_lots:
#                             # If the user disabled both `use_create_lots` and `use_existing_lots`
#                             # checkboxes on the picking type, he's allowed to enter tracked
#                             # products without a `lot_id`.
#                             continue
#                     elif ml.move_id.inventory_id:
#                         # If an inventory adjustment is linked, the user is allowed to enter
#                         # tracked products without a `lot_id`.
#                         continue
#
#                     if not ml.lot_id:
#                         raise UserError(_('You need to supply a lot/serial number for %s.') % ml.product_id.name)
#             elif qty_done_float_compared < 0:
#                 raise UserError(_('No negative quantities allowed'))
#             else:
#                 ml_to_delete |= ml
#         ml_to_delete.unlink()
#
#         # Now, we can actually move the quant.
#         done_ml = self.env['stock.move.line']
#         for ml in self - ml_to_delete:
#             if ml.product_id.type == 'product':
#                 Quant = self.env['stock.quant']
#                 rounding = ml.product_uom_id.rounding
#
#                 # if this move line is force assigned, unreserve elsewhere if needed
#                 if not ml.location_id.should_bypass_reservation() and float_compare(ml.qty_done, ml.product_qty,
#                                                                                     precision_rounding=rounding) > 0:
#                     extra_qty = ml.qty_done - ml.product_qty
#                     ml._free_reservation(ml.product_id, ml.location_id, extra_qty, lot_id=ml.lot_id,
#                                          package_id=ml.package_id, owner_id=ml.owner_id, ml_to_ignore=done_ml)
#                 # unreserve what's been reserved
#                 if not ml.location_id.should_bypass_reservation() and ml.product_id.type == 'product' and ml.product_qty:
#                     try:
#                         Quant._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty,
#                                                         lot_id=ml.lot_id, package_id=ml.package_id,
#                                                         owner_id=ml.owner_id, strict=True)
#                     except UserError:
#                         Quant._update_reserved_quantity(ml.product_id, ml.location_id, -ml.product_qty, lot_id=False,
#                                                         package_id=ml.package_id, owner_id=ml.owner_id, strict=True)
#
#                 # move what's been actually done
#                 quantity = ml.product_uom_id._compute_quantity(ml.qty_done, ml.move_id.product_id.uom_id,
#                                                                rounding_method='HALF-UP')
#                 available_qty, in_date = Quant._update_available_quantity(ml.product_id, ml.location_id, -quantity,
#                                                                           lot_id=ml.lot_id, package_id=ml.package_id,
#                                                                           owner_id=ml.owner_id)
#                 if available_qty < 0 and ml.lot_id:
#                     # see if we can compensate the negative quants with some untracked quants
#                     untracked_qty = Quant._get_available_quantity(ml.product_id, ml.location_id, lot_id=False,
#                                                                   package_id=ml.package_id, owner_id=ml.owner_id,
#                                                                   strict=True)
#                     if untracked_qty:
#                         taken_from_untracked_qty = min(untracked_qty, abs(quantity))
#                         Quant._update_available_quantity(ml.product_id, ml.location_id, -taken_from_untracked_qty,
#                                                          lot_id=False, package_id=ml.package_id, owner_id=ml.owner_id)
#                         Quant._update_available_quantity(ml.product_id, ml.location_id, taken_from_untracked_qty,
#                                                          lot_id=ml.lot_id, package_id=ml.package_id,
#                                                          owner_id=ml.owner_id)
#                 Quant._update_available_quantity(ml.product_id, ml.location_dest_id, quantity, lot_id=ml.lot_id,
#                                                  package_id=ml.result_package_id, owner_id=ml.owner_id, in_date=in_date)
#             done_ml |= ml
#         # Reset the reserved quantity as we just moved it to the destination location.
#         (self - ml_to_delete).with_context(bypass_reservation_update=True).write({
#             'product_uom_qty': 0.00
#         })
#
#
#
# class StockMove(models.Model):
#     _inherit = 'stock.move'
#
#     def _action_done(self):
#         self.filtered(lambda move: move.state == 'draft')._action_confirm()  # MRP allows scrapping draft moves
#         moves = self.exists().filtered(lambda x: x.state not in ('done', 'cancel'))
#         moves_todo = self.env['stock.move']
#
#         # Cancel moves where necessary ; we should do it before creating the extra moves because
#         # this operation could trigger a merge of moves.
#         for move in moves:
#             if move.quantity_done <= 0:
#                 if float_compare(move.product_uom_qty, 0.0, precision_rounding=move.product_uom.rounding) == 0:
#                     move._action_cancel()
#
#         # Create extra moves where necessary
#         for move in moves:
#             if move.state == 'cancel' or move.quantity_done <= 0:
#                 continue
#             # extra move will not be merged in mrp
#             if not move.picking_id:
#                 moves_todo |= move
#             moves_todo |= move._create_extra_move()
#
#         # Split moves where necessary and move quants
#         for move in moves_todo:
#             # To know whether we need to create a backorder or not, round to the general product's
#             # decimal precision and not the product's UOM.
#             rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')
#             if float_compare(move.quantity_done, move.product_uom_qty, precision_digits=rounding) < 0:
#                 # Need to do some kind of conversion here
#                 qty_split = move.product_uom._compute_quantity(move.product_uom_qty - move.quantity_done,
#                                                                move.product_id.uom_id, rounding_method='HALF-UP')
#                 new_move = move._split(qty_split)
#                 for move_line in move.move_line_ids:
#                     if move_line.product_qty and move_line.qty_done:
#                         # FIXME: there will be an issue if the move was partially available
#                         # By decreasing `product_qty`, we free the reservation.
#                         # FIXME: if qty_done > product_qty, this could raise if nothing is in stock
#                         try:
#                             move_line.write({'product_uom_qty': move_line.qty_done})
#                         except UserError:
#                             pass
#                 move._unreserve_initial_demand(new_move)
#             if move.inventory_id:
#                 move.write({'date': move.inventory_id.date})
#             move.move_line_ids._action_done()
#         # Check the consistency of the result packages; there should be an unique location across
#         # the contained quants.
#         for result_package in moves_todo \
#                 .mapped('move_line_ids.result_package_id') \
#                 .filtered(lambda p: p.quant_ids and len(p.quant_ids) > 1):
#             if len(result_package.quant_ids.mapped('location_id')) > 1:
#                 raise UserError(_('You should not put the contents of a package in different locations.'))
#         picking = moves_todo and moves_todo[0].picking_id or False
#         moves_todo.write({'state': 'done'})
#         moves_todo.mapped('move_dest_ids')._action_assign()
#
#         # We don't want to create back order for scrap moves
#         # Replace by a kwarg in master
#         if self.env.context.get('is_scrap'):
#             return moves_todo
#
#         if picking:
#             picking._create_backorder()
#
#         return moves_todo



# class StockInventory(models.Model):
#     _inherit = "stock.inventory"
#
#     def _get_inventory_lines_values(self):
#         # TDE CLEANME: is sql really necessary ? I don't think so
#         locations = self.env['stock.location'].search([('id', 'child_of', [self.location_id.id])])
#         domain = ' location_id in %s'
#         args = (tuple(locations.ids),)
#
#         vals = []
#         Product = self.env['product.product']
#         # Empty recordset of products available in stock_quants
#         quant_products = self.env['product.product']
#         # Empty recordset of products to filter
#         products_to_filter = self.env['product.product']
#
#         # case 0: Filter on company
#         if self.company_id:
#             domain += ' AND company_id = %s'
#             args += (self.company_id.id,)
#
#         # case 1: Filter on One owner only or One product for a specific owner
#         if self.partner_id:
#             domain += ' AND owner_id = %s'
#             args += (self.partner_id.id,)
#         # case 2: Filter on One Lot/Serial Number
#         if self.lot_id:
#             domain += ' AND lot_id = %s'
#             args += (self.lot_id.id,)
#         # case 3: Filter on One product
#         if self.product_id:
#             domain += ' AND product_id = %s'
#             args += (self.product_id.id,)
#             products_to_filter |= self.product_id
#         # case 4: Filter on A Pack
#         if self.package_id:
#             domain += ' AND package_id = %s'
#             args += (self.package_id.id,)
#         # case 5: Filter on One product category + Exahausted Products
#         if self.category_id:
#             categ_products = Product.search([('categ_id', '=', self.category_id.id)])
#             domain += ' AND product_id = ANY (%s)'
#             args += (categ_products.ids,)
#             products_to_filter |= categ_products
#
#         self.env.cr.execute("""SELECT product_id, sum(quantity) as product_qty, location_id, lot_id as prod_lot_id, package_id, owner_id as partner_id
#             FROM stock_quant
#             WHERE %s
#             GROUP BY product_id, location_id, lot_id, package_id, partner_id """ % domain, args)
#
#         for product_data in self.env.cr.dictfetchall():
#             # replace the None the dictionary by False, because falsy values are tested later on
#             for void_field in [item[0] for item in product_data.items() if item[1] is None]:
#                 product_data[void_field] = False
#
#             if product_data['product_id']:
#                 product_data['theoretical_qty'] = Product.browse(product_data['product_id']).with_context(
#                     to_date=self.date).qty_available
#                 product_data['product_qty'] = Product.browse(product_data['product_id']).with_context(
#                     to_date=self.date).qty_available
#                 product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
#                 quant_products |= Product.browse(product_data['product_id'])
#             vals.append(product_data)
#         if self.exhausted:
#             exhausted_vals = self._get_exhausted_inventory_line(products_to_filter, quant_products)
#             vals.extend(exhausted_vals)
#         return vals
#
#     def action_start(self):
#         for inventory in self:
#             vals = {'state': 'confirm'}
#             if (inventory.filter != 'partial') and not inventory.line_ids:
#                 vals.update(
#                     {'line_ids': [(0, 0, line_values) for line_values in inventory._get_inventory_lines_values()]})
#             inventory.write(vals)
#         return True


class StockQuant(models.Model):
    _inherit = "stock.quant"

    lst_price = fields.Float('Sale Price', related='product_id.lst_price')
    cost_price = fields.Float('Cost Price', related='product_id.standard_price')
    amount = fields.Float("Amount", compute='get_total_amount', digits=(12, 3))

    # @api.one
    # @api.depends('inventory_id.date', 'location_id', 'product_id', 'package_id', 'product_uom_id', 'company_id',
    #              'prod_lot_id', 'partner_id')
    # def _compute_theoretical_qty(self):
    #     super(InventoryLine, self)._compute_theoretical_qty()
    #     self.theoretical_qty = self.product_id.with_context(
    #                 to_date=self.inventory_id.date).qty_available

    def _get_quants(self):
        return self.env['stock.quant'].search([
            ('company_id', '=', self.company_id.id),
            ('location_id', '=', self.location_id.id),
            ('lot_id', '=', self.prod_lot_id.id),
            ('product_id', '=', self.product_id.id),
            ('owner_id', '=', self.partner_id.id),
            ('create_date', '<=', self.inventory_id.date),
            ('package_id', '=', self.package_id.id)])

    @api.depends('cost_price', 'inventory_quantity')
    def get_total_amount(self):
        for rec in self:
            rec.amount = rec.cost_price * rec.inventory_quantity
