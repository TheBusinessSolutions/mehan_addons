# -*- encoding: utf-8 -*-

from odoo import fields, models

class MRET(models.Model):
    _name = 'mr.et'

    name = fields.Char("Name", required=True)