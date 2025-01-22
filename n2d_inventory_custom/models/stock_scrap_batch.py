# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _


class ScrapBatch(models.Model):
    _name = 'stock.scrap.batch'

    def _get_default_scrap_location_id(self):
        return self.env['stock.location'].search([('scrap_location', '=', True)], limit=1).id

    def _get_default_location_id(self):
        return self.env.ref('stock.stock_location_stock', raise_if_not_found=False)

    name = fields.Char("Name")
    location_id = fields.Many2one('stock.location', "Location", default=_get_default_location_id,
                                  domain="[('usage', '=', 'internal')]")
    scrap_location_id = fields.Many2one('stock.location', "Scrap Location", default=_get_default_scrap_location_id,
                                        domain="[('scrap_location', '=', True)]")
    scrap_ids = fields.One2many('scrap.batch.line', 'batch_id', string="Scrap Lines")
    state = fields.Selection([('draft', "Draft"), ('done', "Done")], default='draft', string="Status")


    def action_validate(self):
        for rec in self:
            for line in rec.scrap_ids:
                scrap = self.env['stock.scrap'].create({
                    'product_id': line.product_id.id,
                    'product_uom_id': line.product_id.uom_id.id,
                    'scrap_qty': line.scrap_qty,
                    'location_id': rec.location_id.id,
                    'scrap_location_id': rec.scrap_location_id.id,
                    'batch_id': rec.id,
                })
                scrap.action_validate()
            rec.state = 'done'

    def open_scrap(self):
        self.ensure_one()
        scrap_ids = self.env['stock.scrap'].search([('batch_id', '=', self.id)]).ids

        tree_id = self.env.ref('stock.stock_scrap_tree_view').id
        form_id = self.env.ref('stock.stock_scrap_form_view').id
        return {
            'domain': [('id', 'in', scrap_ids)],
            'name': _('Scrap Orders'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'stock.scrap',
            'views': [(tree_id, 'tree'), (form_id, 'form')],
            'type': 'ir.actions.act_window'
        }


class ScrapBatchLine(models.Model):
    _name = 'scrap.batch.line'

    product_id = fields.Many2one('product.product', "Product")
    scrap_qty = fields.Float("Quantity")
    batch_id = fields.Many2one('stock.scrap.batch', "Batch", ondelete='cascade')
