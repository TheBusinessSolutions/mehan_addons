# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'


    def check_identification_end_date(self):
        id_alert_days = self.env['ir.config_parameter'].sudo().get_param('n2d_hr.identification_alert')
        today = fields.Date.today()
        employees = self.with_user(SUPERUSER_ID).search([])
        for rec in employees:
            if rec.identification_expire_date:
                date_end_obj = fields.Date.to_date(rec.identification_expire_date)
                expiry_days = (date_end_obj - today).days
                if expiry_days < int(id_alert_days):
                    if rec.coach_id.user_id.partner_id.id:
                        msg = str(rec.name) + " " + "identification" + " " + " expires soon"
                        rec.message_post(body=msg, partner_ids=[rec.coach_id.user_id.partner_id.id])



    def check_passport_end_date(self):
        passport_alert_days = self.env['ir.config_parameter'].sudo().get_param('n2d_hr.passport_alert')
        today = fields.Date.today()
        employees = self.with_user(SUPERUSER_ID).search([])
        for rec in employees:
            if rec.passport_expire_date:
                date_end_obj = fields.Date.to_date(rec.passport_expire_date)
                expiry_days = (date_end_obj - today).days
                if expiry_days < int(passport_alert_days):
                    if rec.coach_id.user_id.partner_id.id:
                        msg = str(rec.name) + " " + "passport" + " " + " expires soon"
                        rec.message_post(body=msg, partner_ids=[rec.coach_id.user_id.partner_id.id])


