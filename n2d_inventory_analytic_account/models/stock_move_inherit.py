# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        res = super(StockMove, self)._prepare_account_move_line(qty, cost, credit_account_id, debit_account_id, description)
        if res[0][2]['account_id'] == self.product_id.categ_id.property_stock_account_input_categ_id.id or res[0][2]['account_id'] == self.product_id.categ_id.property_stock_account_output_categ_id.id:
            res[0][2]['analytic_account_id'] = self.picking_id.analytic_account.id
        if res[1][2]['account_id'] == self.product_id.categ_id.property_stock_account_input_categ_id.id or res[1][2]['account_id'] == self.product_id.categ_id.property_stock_account_output_categ_id.id:
            res[1][2]['analytic_account_id'] = self.picking_id.analytic_account.id
        return res
