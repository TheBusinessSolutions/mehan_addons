# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from ast import literal_eval


class CashInPetty(models.Model):

    _inherit = 'stock.picking'

    employee_id = fields.Many2one('hr.employee', "Engineering Name")
