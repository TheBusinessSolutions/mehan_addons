# -*-coding: utf-8 -*-

from odoo import models, fields, api


class PurchaseRequest(models.TransientModel):
    _name = 'purchase.request'

    sale_id = fields.Many2one('sale.order')
    order_date = fields.Datetime("Date")
    partner_id = fields.Many2one('res.partner', "Supplier")

    def create_order(self):
        for rec in self:
            if rec.sale_id:
                lines = []
                for line in rec.sale_id.order_line:
                    if line.product_id.type == 'service':
                        name = line.product_id.display_name
                        if line.product_id.description_purchase:
                            name += '\n' + line.product_id.description_purchase

                        lines.append((0, 0, {
                            'product_id': line.product_id.id,
                            'account_analytic_id': rec.sale_id.analytic_account_id.id,
                            'analytic_tag_ids': [(6, 0, line.analytic_tag_ids.ids)],
                            'name': name,
                            'product_uom': line.product_id.uom_id.id,
                            'price_unit': line.product_id.standard_price,
                            'product_qty': line.product_uom_qty,
                            'date_planned': rec.order_date,
                        }))
                model_obj = self.env['sale.order']
                field_info = model_obj.fields_get()
                purchase_id = self.env['purchase.order'].create({
                    'partner_id': rec.partner_id.id,
                    'date_order': rec.order_date,
                    'date_planned': rec.order_date,
                    'company_id': rec.sale_id.company_id.id,
                    'currency_id': rec.sale_id.currency_id.id,
                    'order_line': lines,
                    'sale_order_id': rec.sale_id.id,
                    'origin': rec.sale_id.name,
                    'tcr': str(rec.sale_id.tcr) if field_info.get('tcr') else '',
                })
                if purchase_id:
                    for line in purchase_id.order_line:
                        line._onchange_quantity()
