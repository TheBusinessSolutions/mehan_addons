'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class Employee(models.Model):
    _inherit = 'hr.employee'
    
    name = fields.Char(translate = True)
