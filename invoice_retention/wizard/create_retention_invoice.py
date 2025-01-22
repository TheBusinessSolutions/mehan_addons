# -*- coding: utf-8 -*-
from odoo import api, fields, models, _

class RetentionWizLine(models.TransientModel):
    _name = "retention.wiz.line"

    payment_wiz_id = fields.Many2one('retention.payment.inv', 'Wizard')
    name = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Supplier', required=True)
    invoice_id = fields.Many2one('account.move', 'Invoice')
    line_id = fields.Many2one('retention.line', 'Main WH Line')
    payment_invoice_id = fields.Many2one('account.move', 'Payment Invoice')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    amount = fields.Float(required=True)
    state = fields.Selection([
        ('to_invoice', 'To Invoiced'),
        ('invoiced', 'Invoiced')], index=True, default='to_invoice')



class RetentionPayment(models.TransientModel):
    _name = "retention.payment.inv"
    _description = "Retention Payment Invoice"

    line_ids = fields.One2many('retention.wiz.line', 'payment_wiz_id', string='Retention Lines')
    partner_id = fields.Many2one('res.partner', 'Customer', readonly=True)
    retention_inv_type = fields.Selection([('vendor_bill','Vendor Bill'),('customer_inv','Customer Invoice')],default='customer_inv')
    
    @api.model
    def default_get(self, fields):
        res = super(RetentionPayment, self).default_get(fields)
        vals = []
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        if active_model == 'res.partner':
            domain = [('partner_id', '=', active_id), ('state','=','to_invoice'),('retention_inv_type','=','customer_inv')]
            res.update({'partner_id': active_id})
        lines = self.env['retention.line'].search(domain)
        lines_data = []
        for line in lines:
            lines_data.append((0,0,{
                'name': line.name,
                'partner_id': line.partner_id and line.partner_id.id or False,
                'invoice_id': line.invoice_id and line.invoice_id.id or False,
                'product_id': line.product_id and line.product_id.id or False,
                'payment_invoice_id': line.payment_invoice_id and line.payment_invoice_id.id or False,
                'line_id': line.id,
                'amount': line.amount,
                'state': line.state,
            }))
        res.update({'line_ids': lines_data})
        return res

    
    @api.onchange('retention_inv_type')
    def filter_retention_line_entry(self):
        active_model = self.env.context.get('active_model')
        active_id = self.env.context.get('active_id')
        if active_model == 'res.partner':
            if self.retention_inv_type == 'customer_inv': 
                domain = [('partner_id', '=', active_id), ('state','=','to_invoice'),('retention_inv_type','=','customer_inv')]
            else:
                domain = [('partner_id', '=', active_id), ('state','=','to_invoice'),('retention_inv_type','=','vendor_bill')]
                 
        lines = self.env['retention.line'].search(domain)
        lines_data = []
        self.line_ids = False
        for line in lines:
            lines_data.append((0,0,{
                'name': line.name,
                'partner_id': line.partner_id and line.partner_id.id or False,
                'invoice_id': line.invoice_id and line.invoice_id.id or False,
                'product_id': line.product_id and line.product_id.id or False,
                'payment_invoice_id': line.payment_invoice_id and line.payment_invoice_id.id or False,
                'line_id': line.id,
                'amount': line.amount,
                'state': line.state,
            }))
        self.write({'line_ids': lines_data})


    def create_invoice(self):
        inv_obj = self.env['account.move']
        inv_line_obj = self.env['account.move.line']
        for line in self.line_ids:
            account_id = False
            if line.product_id and self.retention_inv_type == 'customer_inv':
                account_id = line.product_id.property_account_income_id.id
            if line.product_id and self.retention_inv_type == 'vendor_bill':
                account_id = line.product_id.property_account_expense_id.id    
            if self.retention_inv_type == 'customer_inv':
                move_type = 'out_invoice'
            if self.retention_inv_type == 'vendor_bill':
                move_type = 'in_invoice'    
            if not account_id:
                prop = self.env['ir.property']._get('property_account_income_categ_id', 'product.category')
                account_id = prop and prop.id or False
            inv_line_obj = {
                'name': line.name,
                'price_unit': line.amount,
                'account_id': account_id,
                'quantity': 1.0,
                'product_uom_id': line.product_id.uom_id.id,
                'product_id': line.product_id.id,
                'analytic_account_id': False,
                
            }
            invoice = inv_obj.create({ 'partner_id': self.partner_id.id,
                                        'move_type': move_type,
                                        'currency_id': self.env.user.company_id.currency_id.id,
                                        'invoice_line_ids':[(0,0,inv_line_obj)]})
            
            line.line_id.write({'payment_invoice_id' : invoice.id,
                        'state' : 'invoiced'})
        return invoice

    
    def create_and_view_invoice(self):
        invoice = self.create_invoice()
        imd = self.env['ir.model.data']
        action = self.env.ref('account.action_move_out_invoice_type')
        list_view_id = self.env.ref('account.view_out_invoice_tree').id
        form_view_id = self.env.ref('account.view_move_form').id

        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'views': [[form_view_id, 'form'], [list_view_id, 'tree']],
            'target': action.target,
            'context': action.context,
            'res_model': action.res_model,
            'res_id': invoice.id,
        }
        return result
