# -*- encoding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class AccountAnalytic(models.Model):
    _inherit = 'account.analytic.account'

    database_db_account = fields.Char("DB")
    region = fields.Many2one('region.name', string="Region")

    site_id = fields.Char("Site ID", required=1)
    project_name = fields.Many2one('project.name', string="Project name", required=1)
    request_date = fields.Date("Requested Date")
    sequence = fields.Char()
    # strap_tag_id = fields.Many2one('account.analytic.tag', string="PO")


    # @api.constrains('tag_ids')
    # def check_values_tags(self):
    #     for val in self:
    #         if len(val.tag_ids) > 1:
    #             raise ValidationError(_("Sorry .. 'Enter One Tag only' !!"))

    @api.model
    def create(self, vals):
        site = vals.get('site_id') or ''
        vals['sequence'] = site + self.env['ir.sequence'].next_by_code('account.analytic.account')
        return super(AccountAnalytic, self).create(vals)


class AccountAnalyticTag(models.Model):
    _inherit = 'account.analytic.tag'

    description = fields.Text("Description")
    frame_agreement = fields.Char("Frame Agreement")
    amount = fields.Float("Amount")
