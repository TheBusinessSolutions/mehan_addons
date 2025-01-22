'''
Created on Feb 22, 2021

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class HrEmployeePublic(models.Model):
    _inherit = "hr.employee.public"
        
    name = fields.Char(compute = '_calc_name', store = True, translate = True, compute_sudo = True)
    
    @api.depends('resource_id.name')
    @api.depends_context('lang')
    def _calc_name(self):
        for record in self:
            record.name = record.resource_id.name

    @api.model
    def _recompute_name(self):
        records = self.search([])
        self.env.add_to_compute(self._fields['name'], records)
        self.flush()
        