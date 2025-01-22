# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, _


class HRContract(models.Model):
    _name = 'hr.contract'
    _inherit = 'hr.contract'


    def check_contract_expiry_date(self):
        contract_alert_days = self.env['ir.config_parameter'].sudo().get_param('general_changes.contract_alert')
        today = fields.Date.today()
        contracts = self.with_user(SUPERUSER_ID).search([('state', '=', 'open'), ('date_end', '!=', False)])
        for rec in contracts:
            date_end_obj = fields.Date.to_date(rec.date_end)
            expiry_days = (date_end_obj - today).days
            if expiry_days < int(contract_alert_days):
                if rec.hr_responsible_id.partner_id.id:
                    msg = _('%(employee)s contract expires in less than 2 months', employee=rec.employee_id.name)
                    rec.message_post(body=msg, partner_ids=[rec.hr_responsible_id.partner_id.id])


