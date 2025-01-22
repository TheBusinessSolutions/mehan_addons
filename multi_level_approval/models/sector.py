# -*- encoding: utf-8 -*-

from odoo import models, fields, api

class SectorForm(models.Model):
    _name = "sector"
    name = fields.Char(string='Name', required=True)