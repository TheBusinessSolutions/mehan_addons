# -*- coding: utf-8 -*-

from odoo import fields, models, api, _
from odoo.exceptions import UserError


class RetentionFee(models.Model):
    _name = 'retention.line'

    name = fields.Char()
    partner_id = fields.Many2one('res.partner', 'Supplier', required=True)
    retention_inv_type = fields.Selection([('vendor_bill','Vendor Bill'),('customer_inv','Customer Invoice')])
    invoice_id = fields.Many2one('account.move', 'Invoice')
    payment_invoice_id = fields.Many2one('account.move', 'Payment Invoice')
    product_id = fields.Many2one('product.product', 'Product', required=True)
    amount = fields.Float(required=True)
    state = fields.Selection([
        ('to_invoice', 'To Invoiced'),
        ('invoiced', 'Invoiced')], index=True, default='to_invoice')

   
    def unlink(self):
        for line in self:
            if line.state == 'invoiced':
                raise UserError(_('You can not delete a invoiced retention fee.'))
        return super(RetentionFee, self).unlink()

    

class ResPartner(models.Model):
    _inherit = "res.partner"

    def _retention_count(self):
        for rec in self:
            rec.retention_count = self.env['retention.line'].search_count([('partner_id','=',rec.id),('retention_inv_type','=','vendor_bill')])
            
    def _retention_count_customer_inv(self):
        for rec in self:
            rec.retention_count_customer_inv = self.env['retention.line'].search_count([('partner_id','=',rec.id),('retention_inv_type','=','customer_inv')])        

    retention_count = fields.Integer(compute="_retention_count", readonly=True, string="Supplier Retentions")
    retention_count_customer_inv = fields.Integer(compute="_retention_count_customer_inv", readonly=True, string="Customer Retentions")
    retention_ids = fields.One2many('retention.line', 'partner_id', string='Retention Lines', copy=False)

    def partner_retention_action(self):
        return {
            'name': _('With Retentions'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'retention.line',
            'type': 'ir.actions.act_window',
            'domain': [('id','in', self.retention_ids.ids),('retention_inv_type','=', 'vendor_bill')],
            'context': {
                'default_partner_id': self.id,
            }
        }

    def partner_retention_customer_inv_action(self):
        return {
            'name': _('With Retentions'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'retention.line',
            'type': 'ir.actions.act_window',
            'domain': [('id','in', self.retention_ids.ids),('retention_inv_type','=', 'customer_inv')],
            'context': {
                'default_partner_id': self.id,
            }
        }        


class InvoiceLine(models.Model):
    _inherit = "account.move.line"

    retention_id = fields.Many2one('retention.line', string='With Retention Line', copy=False)

  
        
class Invoice(models.Model):
    _inherit = "account.move"

    retention_ids = fields.One2many('retention.line', 'invoice_id', string='With Retention Fees', copy=False)
    retention_fee = fields.Boolean("Add Retention Fee", readonly=True, states={'draft': [('readonly', False)]},)

    def action_invoice_open(self):
        res = super(Invoice, self).action_invoice_open()
        lines = self.env['retention.line'].search([('invoice_id', 'in', self.ids)])
        for line in lines:
            line.name = line.name + ' ' + line.invoice_id.number
        return res

    def _retention_unset(self):
        retention_product = self.env.user.company_id.retention_product_id
        if retention_product:
            inv_line = self.invoice_line_ids.filtered(lambda x:x.product_id.id == retention_product.id)
            if inv_line:
                inv_line.with_context(check_move_validity=False).unlink()
            self.env['retention.line'].search([('invoice_id', 'in', self.ids)]).unlink()

    def create_retention(self):
        InvoiceLine = self.sudo().env['account.move.line']
        

        product_id =self.env.user.company_id.retention_product_id# self.sudo().env['res.config.settings'].search([],order='id desc',limit=1).retention_product_id
        retention_percentage =self.env.user.company_id.retention_percentage# self.sudo().env['res.config.settings'].search([],order='id desc',limit=1).retention_percentage
        if not product_id:
            raise UserError(_('Please set Retention Fee Product in General Settings first.'))

        self._retention_unset()

        if self.move_type == 'out_invoice':
            account_id = product_id.property_account_income_id.id
        if self.move_type == 'in_invoice':    
            account_id = product_id.property_account_expense_id.id
        
        if not account_id:
            prop = product_id.categ_id.property_account_expense_categ_id
            account_id = prop and prop.id or False

        for invoice in self:
            taxes = product_id.taxes_id.filtered(lambda t: t.company_id.id == invoice.company_id.id)
            taxes_ids = taxes.ids
            if invoice.partner_id and self.fiscal_position_id:
                taxes_ids = self.fiscal_position_id.map_tax(taxes, product_id, invoice.partner_id).ids

            amount = -(invoice.amount_untaxed * retention_percentage)/100
            
            
            InvoiceLine = {
                'name':  'Retention Fees',
                'move_id': invoice.id,
                'price_unit': amount,
                'account_id': account_id,
                'quantity': 1.0,
                'product_uom_id': product_id.uom_id.id,
                'product_id': product_id.id,
                'tax_ids': [(6, 0, taxes_ids)],
            }
            invoice.write({'invoice_line_ids':[(0,0,InvoiceLine)]})
            
        return True


        
