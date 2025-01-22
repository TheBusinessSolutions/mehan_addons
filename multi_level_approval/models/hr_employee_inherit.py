# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrEmoloyee(models.Model):
    _inherit = 'hr.employee'

    state = fields.Selection([('draft', 'Draft'), ('approved', 'approved')], default='draft')
    administration = fields.Many2one('administration', string='Administration')
    sector = fields.Many2one('sector', string='Sector')

    def approve(self):
        for rec in self:
            rec.state = 'approved'

    def write(self, vals):
        if not vals.get('state'):
            vals['state'] = 'draft'
        return super(HrEmoloyee, self).write(vals)