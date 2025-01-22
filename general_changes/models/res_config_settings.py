# -*- coding: utf-8 -*-

from odoo import fields, models, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    contract_alert_days = fields.Integer(string='Contract Alert Days', config_parameter='general_changes.contract_alert')




