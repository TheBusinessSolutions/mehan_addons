# -*- coding: utf-8 -*-

from odoo import api, fields, models, _

class AccountMove(models.Model):
    _inherit='account.move'
    
    def action_post(self):
        res = super(AccountMove,self)._post(soft=False)
        WithretentionLine = self.env['retention.line']
        for inv in self:
            if inv.retention_fee:
                for line in inv.invoice_line_ids:
                    if self.env.user.company_id.retention_product_id and (line.product_id.id == self.env.user.company_id.retention_product_id.id):
                        #Create retention line
                        retention_type = ''
                        if inv.move_type == 'in_invoice':
                            retention_type = 'vendor_bill'
                        if inv.move_type == 'out_invoice':
                            retention_type = 'customer_inv'    
                        wh_line = WithretentionLine.create({
                            'name': line.name,
                            'product_id': line.product_id.id,
                            'partner_id': inv.partner_id.id,
                            'amount': -line.price_subtotal,
                            'invoice_id': inv.id,
                            'retention_inv_type':retention_type,
                        })
                        line.retention_id = wh_line.id
        return res
    
     
  
    
    
    
    