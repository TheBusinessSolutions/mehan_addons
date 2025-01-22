from odoo import api, fields, models, _



class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    product_packaging_id = fields.Many2one('product.packaging', string='Packaging')
    product_packaging_qty = fields.Float('Packaging Quantity')





class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"


    def _prepare_invoice_line(self, **optional_values):
        res = super(SaleOrderLine, self)._prepare_invoice_line(**optional_values)
        res.update({'product_packaging_id': self.product_packaging_id.id,
                    'product_packaging_qty': self.product_packaging_qty})
        return res
