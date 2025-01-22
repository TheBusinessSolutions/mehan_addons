# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    resume_alert_days = fields.Integer(string='Resume Alert Days', config_parameter='n2d_hr_doc.resume_alert')




