# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

from odoo import fields, api, models


class ResConfigSettings(models.TransientModel):
    """Class inherit for adding some configuration."""

    _inherit = 'res.config.settings'

    auto_leave_allocation = fields.Boolean(string='Automatically Leave Allocate ?')
    holiday_status_id = fields.Many2many('hr.leave.type', string="Leave Types")

    @api.model
    def default_get(self, fields):
        """Function call for get default value."""
        res = super(ResConfigSettings, self).default_get(fields)
        for data in self.search([]):
            res.update({
                'auto_leave_allocation' : data.auto_leave_allocation,
                'holiday_status_id' : data.holiday_status_id.ids
            })
        return res
