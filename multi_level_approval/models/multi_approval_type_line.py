# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright Domiup (<http://domiup.com>).
#
##############################################################################

from odoo import api, models, fields
import logging

_logger = logging.getLogger(__name__)


class MultiApprovalTypeLine(models.Model):
    _name = 'multi.approval.type.line'
    _description = 'Multi Aproval Type Lines'
    _order = 'sequence'

    name = fields.Char(string='Title', required=True)
    user_id = fields.Many2one(string='User', comodel_name="res.users",
                              )
    sequence = fields.Integer(string='Sequence')
    head_approve = fields.Selection(
        [('direct_manager', 'Direct Manager'),
         ('department_manager', 'Department Manager')], default='direct_manager')
    group_id = fields.Many2one('res.groups', string='Group')
    require_opt = fields.Selection(
        [('Required', 'Required'),
         ('Optional', 'Optional'),
         ], string="Type of Approval", default='Required')
    type_id = fields.Many2one(
        string="Type", comodel_name="multi.approval.type")

    def get_user(self):
        self.ensure_one()
        if self.user_id:
            return self.user_id.id
        else:
            return False

class MultiCertificateTypeLine(models.Model):
    _name = 'multi.certificate.type.line'

    cer_name = fields.Many2one('multi.certificate',string='Name', required=True)
    cer_num = fields.Integer(string='Number', required=True)
    type_id = fields.Many2one(
        string="Type", comodel_name="multi.approval")
