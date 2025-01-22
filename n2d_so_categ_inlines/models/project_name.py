# -*- encoding: utf-8 -*-

from odoo import models, fields


class ProjectName(models.Model):

    _name = 'project.name'

    name = fields.Char(string="name", required=1)

