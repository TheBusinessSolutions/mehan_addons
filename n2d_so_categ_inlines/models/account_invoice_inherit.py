# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AccountInvoice(models.Model):
    _inherit = 'account.move'

    description_from_analytic_tag = fields.Text(string="Description From Analytic Tag")


class AccountInvoiceLine(models.Model):
    _inherit = 'account.move.line'

    @api.constrains('analytic_tag_ids')
    def validate_po(self):
        for rec in self:
            lines = self.env['account.move.line'].search([('move_id', '=', rec.move_id.id)])
            po = lines.mapped('analytic_tag_ids')
            if len(po) > 1:
                raise ValidationError("You can not create invoice lines in same invoice with diffrent po!")
