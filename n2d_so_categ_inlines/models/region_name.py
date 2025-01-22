# -*- encoding: utf-8 -*-

from odoo import models, fields


class Region(models.Model):

    _name = 'region.name'

    name = fields.Char(string="name", required=1)

