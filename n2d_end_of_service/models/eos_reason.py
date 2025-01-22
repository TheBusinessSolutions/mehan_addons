# -*- encoding: utf-8 -*-

from odoo import models, fields


class EOSReason(models.Model):
    _name = 'eos.reason'

    name = fields.Char("Reason", required=1)
    calc_eos = fields.Boolean("Calculate E.O.S?")
