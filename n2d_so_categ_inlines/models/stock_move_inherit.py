# -*- encoding: utf-8 -*-

from odoo import models, fields, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    line = fields.Char("Line")
    sub_inventory = fields.Char("Sub Inventory")
    site = fields.Char("Site ID")
    move_no = fields.Integer("Move No.")
    dor_type = fields.Selection([('do', "DO"), ('ro', "RO")], string='Dor Type', related='picking_id.dor_type', store=1)
    dor_no = fields.Char("Dor Number", related='picking_id.dor_no', store=1)

    mr_id = fields.Many2one('mr.et', "ET Owner", related='picking_id.mr_id', store=1)
    stp_owner = fields.Many2one('sale.rfi', "Stp Owner", related='picking_id.stp_owner', store=1)
    owner_partner_id = fields.Many2one("res.partner", "Transfer Owner", related='picking_id.owner_partner_id', store=1)

    @api.onchange('product_id', 'picking_code')
    def onchange_product_id(self):
        product = self.product_id.with_context(lang=self.partner_id.lang or self.env.user.lang)
        print("picking_code", self.picking_id.picking_type_id.code)
        if self.picking_id.picking_type_id.code == 'internal':
            self.name = product.description_picking
        elif self.picking_id.picking_type_id.code == 'outgoing':
            self.name = product.description_pickingout
        elif self.picking_id.picking_type_id.code == 'incoming':
            self.name = product.description_pickingin
        else:
            self.name = product.partner_ref

        self.product_uom = product.uom_id.id
        return {'domain': {'product_uom': [('category_id', '=', product.uom_id.category_id.id)]}}

    def _prepare_account_move_line(self, qty, cost, credit_account_id, debit_account_id, description):
        res = super(StockMove, self)._prepare_account_move_line(
            qty, cost, credit_account_id, debit_account_id, description
        )
        res[0][2]['analytic_account_id'] = self.picking_id.analytic_account.id
        return res

class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'

    line = fields.Char("Line", )
    sub_inventory = fields.Char("Sub Inventory")
    name = fields.Char("Description",related='product_id.partner_ref',store=True)

    site = fields.Char("Site ID", related='move_id.site', store=1)
    move_no = fields.Integer("Move No.", related='move_id.move_no', store=1)
    dor_type = fields.Selection([('do', "DO"), ('ro', "RO")], string='Dor Type', related='move_id.dor_type', store=1)
    dor_no = fields.Char("Dor Number", related='move_id.dor_no', store=1)

    mr_id = fields.Many2one('mr.et', "ET Owner", related='move_id.mr_id', store=1)
    stp_owner = fields.Many2one('sale.rfi', "Stp Owner", related='move_id.stp_owner', store=1)
    owner_partner_id = fields.Many2one("res.partner", "Transfer Owner", related='move_id.owner_partner_id', store=1)
