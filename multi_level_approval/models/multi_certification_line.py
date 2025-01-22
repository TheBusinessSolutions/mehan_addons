
from odoo import api, models, fields
import logging

class MultiCertificate(models.Model):
    _name = 'multi.certificate'
    _rec_name = 'certification_name'

    certification_name = fields.Char(string='Name', required=True)