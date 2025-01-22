# -*- encoding: utf-8 -*-

from odoo import models, fields, api

class AdministrationForm(models.Model):
    _name = "administration"
    name = fields.Char(string='Name', required=True)