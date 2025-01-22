'''
Created on Dec 10, 2018

@author: Zuhair Hammadi
'''
from odoo import models, fields

class ResourceResource(models.Model):
    _inherit = "resource.resource"

    name = fields.Char(translate = True)