'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields, api

class Department(models.Model):
    _inherit = "hr.department"

    name = fields.Char(translate = True)
    complete_name = fields.Char(translate = True)    
        
    @api.model
    def _recompute_complete_name(self):
        records = self.search([])._hierarchical_sort()
        self.env.add_to_compute(self._fields['complete_name'], records)
        self.flush()    