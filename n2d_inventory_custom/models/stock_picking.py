# -*- encoding: utf-8 -*-

from odoo import fields, models, api


class Picking(models.Model):
    _inherit = "stock.picking"

    is_return = fields.Boolean("Is Return?")

    @api.model
    def create(self, vals):
        # TDE FIXME: clean that brol
        defaults = self.default_get(['name', 'picking_type_id'])
        if not vals.get('is_return') and vals.get('name', '/') == '/' and defaults.get('name', '/') == '/' and vals.get('picking_type_id',
                                                                                          defaults.get(
                                                                                                  'picking_type_id')):
            vals['name'] = self.env['stock.picking.type'].browse(
                vals.get('picking_type_id', defaults.get('picking_type_id'))).sequence_id.next_by_id()
        if vals.get('is_return'):
            vals['name'] = self.env['ir.sequence'].next_by_code('stock.return.picking')

        # TDE FIXME: what ?
        # As the on_change in one2many list is WIP, we will overwrite the locations on the stock moves here
        # As it is a create the format will be a list of (0, 0, dict)
        if vals.get('move_lines') and vals.get('location_id') and vals.get('location_dest_id'):
            for move in vals['move_lines']:
                if len(move) == 3:
                    move[2]['location_id'] = vals['location_id']
                    move[2]['location_dest_id'] = vals['location_dest_id']
        res = super(Picking, self).create(vals)
        res._autoconfirm_picking()
        return res

    # @api.multi
    # def write(self, vals):
    #
    #     defaults = self.default_get(['name', 'picking_type_id'])
    #     if vals.get('is_return'):
    #         vals['name'] = self.env['ir.sequence'].next_by_code('stock.return.picking')
    #     else:
    #         vals['name'] = self.env['stock.picking.type'].browse(
    #             vals.get('picking_type_id', defaults.get('picking_type_id'))).sequence_id.next_by_id()
    #     res = super(Picking, self).write(vals)
    #     return res


