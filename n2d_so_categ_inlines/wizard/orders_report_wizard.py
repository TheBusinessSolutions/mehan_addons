# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError

class OrderReportWizard(models.TransientModel):

    _name = "wizard.orders_report_wizard"

    date_from = fields.Datetime(string="Date From", required=True)
    date_to = fields.Datetime(string="Date To", required=True)
    tcr = fields.Char("TCR")
    database_db = fields.Char("DB")
    status = fields.Selection([('draft', "Quotation"), ('done', "Done")], "Status", default='done')


    @api.constrains('date_from', 'date_to')
    def date_values(self):
        for rec in self:
            if rec.date_from > rec.date_to:
                raise ValidationError('Date from must be less than date to')

    def get_report(self):
        return self.env.ref('n2d_so_categ_inlines.order_report_xlsx_id').report_action(self)