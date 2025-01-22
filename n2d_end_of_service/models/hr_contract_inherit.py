# -*- encoding: utf-8 -*-

from odoo import models, fields


class Contract(models.Model):
    _inherit = 'hr.contract'

    contract_type = fields.Selection([('limited', 'Limited'), ('unlimited', 'UN Limited')], "Type")
    payment_type = fields.Selection(
        [('hourly', "Hourly"), ('daily', "Daily"), ('weekly', "Weekly"), ('monthly', "Monthly"),
         ('by_unit', "By Unit")], "Payment Type")
