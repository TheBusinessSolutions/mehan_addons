# -*- encoding: utf-8 -*-

from odoo import fields, models, api

class ReturnPicking(models.TransientModel):
    _inherit = 'stock.return.picking'

    def _create_returns(self):
        new_picking_id, pick_type_id = super(ReturnPicking, self)._create_returns()
        picking_id = self.env['stock.picking'].browse(new_picking_id)
        picking_id.name = self.env['ir.sequence'].next_by_code('stock.return.picking')
        picking_id.is_return = True
        return picking_id.id, pick_type_id