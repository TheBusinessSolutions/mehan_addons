# -*- coding: utf-8 -*-

from odoo import models, fields, api

class HrContract(models.Model):
    _inherit = 'hr.contract'

    accom = fields.Integer('Accommodation')
    trans = fields.Integer('Transportation')
    mobi = fields.Integer('Mobile')
    food = fields.Integer('Food')
    nature = fields.Integer('Nature Of Work')
    bonus = fields.Float(string="Bonus")
    other = fields.Float(string="Other")
    total_wage = fields.Float("Total Wage", compute='get_total_wage')
    status = fields.Selection([('company', 'Company'), ('outside_company', 'Outside Company')])

    @api.depends('accom', 'trans', 'mobi', 'food', 'nature', 'bonus', 'other', 'wage')
    def get_total_wage(self):
        for rec in self:
            rec.total_wage = rec.accom + rec.trans + rec.mobi + rec.food + rec.nature + rec.bonus + rec.other + rec.wage

    def get_total_allowance(self):
        for rec in self:
            total = rec.accom + rec.trans + rec.mobi + rec.food + rec.nature + rec.bonus + rec.other
        return total