# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    cate_id = fields.Many2one('product.category', store=True, string="Category")
    # strap_tag_id = fields.Many2one('account.analytic.tag', string="PO", related='order_id.analytic_account_id.strap_tag_id')



    @api.constrains('analytic_tag_ids', 'price_total')
    def validate_tag_amount(self):
        for rec in self:
            if len(rec.analytic_tag_ids) > 1:
                raise ValidationError(_("Sorry .. 'Enter One Tag only' !!"))
            if rec.analytic_tag_ids:
                lines = self.env['sale.order.line'].search([('analytic_tag_ids', '=', rec.analytic_tag_ids.ids)])
                total = 0
                for line in lines:
                    total += line.price_total
                if rec.analytic_tag_ids[0].amount < total:
                    raise ValidationError("You Try To Exceed Po Amount!")

    @api.onchange('product_id')
    def product_id_change(self):
        result = super(SaleOrderLine, self).product_id_change()

        self.update({'name': self.product_id.description_sale})

        return result


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    tcr = fields.Char("TCR")
    database_db = fields.Char("DB")
    site_id = fields.Char("Site ID")
    request_date = fields.Date("Requested Date")
    status = fields.Selection(
        [('ongoing', "Ongoing"),('cancelled', "Cancelled"), ('done', "Done"), ('poc_confirmed', "POC Confirmed"),
         ('invited', "Invited"), ('rejected', "Rejected"), ('accepted', "Accepted"),
         ('hold', "Hold")], string="RFI", default='ongoing')
    mr_id = fields.Many2one('mr.et', "ET Owner")
    subcontractor_id = fields.Many2one('sub.contractor', "Subcontractor")
    rfi_id = fields.Many2one('sale.rfi', "RFI")
    done_date = fields.Datetime('Done Date')

    def action_confirm(self):
       for order in self:
            if not order.done_date:
                raise ValidationError("Please Add Done Date!!")
       super(SaleOrder, self).action_confirm()

    @api.constrains('analytic_account_id')
    def validate_analytic_account(self):
        for rec in self:
            if rec.analytic_account_id:
                sale_ids = self.env['sale.order'].search([('analytic_account_id', '=', rec.analytic_account_id.id)])
                if sale_ids and len(sale_ids) > 1:
                    raise ValidationError("Analytic Account Available Only For One Sales Order")

    @api.onchange('analytic_account_id')
    def onchange_analytic_account(self):
        for rec in self:
            rec.tcr = rec.analytic_account_id.name
            rec.database_db = rec.analytic_account_id.database_db_account
            rec.site_id = rec.analytic_account_id.site_id
            rec.request_date = rec.analytic_account_id.request_date
            # for line in rec.order_line:
            #     line.analytic_tag_ids = [(6, 0, rec.analytic_account_id.tag_ids.ids)]

