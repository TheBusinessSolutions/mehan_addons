# -*- encoding: utf-8 -*-
from docutils.nodes import field

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CashFromPettyBatch(models.Model):
    _name = 'petty.batch'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'employee_id'

    state = fields.Selection(
        [('draft', "Draft"), ('approved', "Approved"), ('confirmed', "Confirmed"), ('rejected', "Rejected"), ('cancelled', "Cancelled")],
        default='draft', string="Status")
    employee_id = fields.Many2one('hr.employee', "Employee", ondelete='cascade', domain=[('user_id', '!=', False)])
    partner_id = fields.Many2one('res.partner', "Vendor")
    line_ids = fields.One2many('petty.batch.line', 'batch_id', "Lines")
    sequence = fields.Char(string='Petty Batch ID', readonly=True)
    total = fields.Float("Total Amount", compute="_total_amount")
    batch_date = fields.Date('Batch Date')
    document_id = fields.Char('Document ID')

    @api.depends('line_ids.amount')
    def _total_amount(self):
        for rec in self:
            rec.total = 0
            for line in rec.line_ids:
               rec.total += line.amount
            print(rec.total)
    def action_open(self):
        for rec in self:
            petty_ids = self.env['cash.from.petty'].search([('batch_id', '=', rec.id)]).ids
            return {
                'domain': [('id', 'in', petty_ids)],
                'name': _('Purchase Petty'),
                'view_type': 'form',
                'view_mode': 'tree,form',
                'res_model': 'cash.from.petty',
                'type': 'ir.actions.act_window',
            }

    def action_confirm(self):
        for rec in self:
            for line in rec.line_ids:
                petty_obj = self.env['cash.from.petty'].create({
                    'employee_id': rec.employee_id.id,
                    'partner_id': rec.partner_id.id,
                    'amount': line.amount if not line.product_id else line.total,
                    'analytic_account_id': line.analytic_account_id.id,
                    'lab': line.label,
                    'account_id': line.account_id.id,
                    'batch_id': rec.id,
                    'batch_date': rec.batch_date,

                })
                petty_obj.action_approve()
                petty_obj.action_confirm()
            rec.state = 'confirmed'

    def action_approve(self):
        for rec in self:
            rec.state = 'approved'

    def action_reject(self):
        for rec in self:
            rec.state = 'rejected'


    def action_cancel(self):
        for rec in self:
            for line in rec.line_ids:
                petty_obj = self.env['cash.from.petty'].search([('batch_id', '=', rec.id)])
                petty_obj.move_id.sudo().button_draft()
                petty_obj.move_id.sudo().button_cancel()
                petty_obj.sudo().unlink()
            rec.state = 'cancelled'

    @api.model
    def create(self, vals):
        vals['sequence'] = self.env['ir.sequence'].next_by_code('petty.sequence') or ''
        return super(CashFromPettyBatch, self).create(vals)


class CashFromPettyBatchLine(models.Model):
    _name = 'petty.batch.line'

    amount = fields.Float("Amount")
    account_id = fields.Many2one("account.account", "Account")
    label = fields.Text('Label')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account')
    batch_id = fields.Many2one('petty.batch', "Batch")
    product_id = fields.Many2one('product.product', string='Product')
    price = fields.Float("Price")
    quantity = fields.Float("Quantity")
    discount = fields.Float("Discount")
    tax_id = fields.Many2many('account.tax', string='VAT')
    sub_total = fields.Float("Sub Total", compute="_sub_total")
    total = fields.Float("Total", compute="_total")
    description = fields.Char(string='Description')
    partner_id = fields.Many2one('res.partner', "Vendor", track_visibility='onchange')
    po_id = fields.Many2one('purchase.order', "Purchase Order")
    product_type = fields.Selection(string="Product Type",  related='product_id.type')
    current_date = fields.Datetime("Current Date")

    def create_o(self):
        for line in self:
            if line.partner_id.id:
                purchase_order = self.env['purchase.order'].search(
                    [('partner_id', '=', line.partner_id.id), ('state', '=', 'draft')],
                    limit=1)
                if purchase_order:
                    x = self.env['purchase.order.line'].create(
                        {
                            'order_id': purchase_order.id,
                            'product_id': line.product_id.id,
                            'name': "Petty cash",
                            'product_qty': line.quantity,
                            'price_unit': line.price,
                            'product_uom': line.product_id.uom_id.id,
                            'date_planned': fields.Date.today(),
                            'petty_batch_line': line.batch_id.id,
                        })
                    line.po_id = purchase_order.id


                    print('Create New line in Purchase Order',  line.po_id)

                else:
                    lines = []
                    lines.append(
                        (0, 0,
                         {
                             'product_id': line.product_id.id,
                             'name': "Petty cash",
                             'product_qty': line.quantity,
                             'price_unit': line.price,
                             'product_uom': line.product_id.uom_id.id,
                             'date_planned': fields.Date.today(),
                             'petty_batch_line': line.batch_id.id,
                         }
                         )
                    )
                    values = {
                        'date_order': fields.Datetime.now(),
                        'date_planned': fields.Date.today(),
                        'partner_id': line.partner_id.id,
                        'order_line': lines,
                    }
                    if not line.product_id:
                        raise ValidationError("Please Enter Product")

                    line_id = self.env['purchase.order'].create(values)
                    line.po_id = line_id.id
                    print(line.po_id)
                    # line.state = 'confirm'
                    # print('Create New Purchase Order')
            else:
                raise ValidationError("Please Enter Vendor Name")

    @api.depends('price', 'quantity')
    @api.onchange('price', 'quantity')
    def _sub_total(self):
        for rec in self:
            rec.sub_total = (rec.price * rec.quantity)

    @api.depends('tax_id', 'sub_total', 'discount')
    @api.onchange('tax_id', 'sub_total', 'discount')
    def _total(self):
        for rec in self:
            total_tax = 0
            for tax in rec.tax_id:
                total_tax += tax.amount

            rec.total = rec.sub_total + (total_tax / 100 * rec.sub_total) - rec.discount
            # print('total_tax', total_tax)

    
    # def print_report(self):
    #     data = {
    #         'model':'n2d_petty_cash.petty_batch_form',
    #         'form': self.read()[0]
    #     }
    #     return self.env.ref('n2d_petty_cash.petty_batch').with_context(landscape=True).report_action(self, data=data)
        


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'


    petty_batch_line = fields.Many2one('petty.batch')