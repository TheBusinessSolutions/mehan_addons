# -*- coding: utf-8 -*-

from odoo import models, fields, SUPERUSER_ID, _


class ResumeLine(models.Model):
    _inherit = 'hr.resume.line'


    def check_resume_end_date(self):
        resume_alert_days = self.env['ir.config_parameter'].sudo().get_param('n2d_hr_doc.resume_alert')
        today = fields.Date.today()
        resumes = self.with_user(SUPERUSER_ID).search([])
        for rec in resumes:
            if rec.date_end:
                date_end_obj = fields.Date.to_date(rec.date_end)
                expiry_days = (date_end_obj - today).days
                if expiry_days < int(resume_alert_days):
                    if rec.employee_id.coach_id.user_id.partner_id.id:
                        msg = _('%(employee)s %(education)s ends soon', employee=rec.employee_id.name , education=rec.name)
                        rec.employee_id.message_post(body=msg, partner_ids=[rec.employee_id.coach_id.user_id.partner_id.id])


