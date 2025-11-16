# -*- coding: utf-8 -*-

from odoo import models, fields, api, SUPERUSER_ID, _



class beneficiary_disbursement_permission(models.Model):
    _name = 'beneficiary.disbursement.permission'
    # _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'beneficiary.disbursement.permission'

    name = fields.Char(string="Permission Number", readonly=True, required=True, copy=False, default='New')
    mustfid_id = fields.Many2one('death.beneficiaries.lines', domain="[('state', '=', 'done')]")
    dead_id = fields.Many2one('deceased.info', related='mustfid_id.dead_id')
    national_id = fields.Char(related='mustfid_id.national_id')


    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code(
                'self.permissionno') or 'New'
        result = super(beneficiary_disbursement_permission, self).create(vals)
        return result
