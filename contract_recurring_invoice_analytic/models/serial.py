# -*- coding: utf-8 -*-

import datetime
from datetime import date, timedelta as td
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, tools, _
from odoo.tools.misc import formatLang, format_date
from odoo.exceptions import ValidationError, Warning, UserError


class CustomSerialNumber(models.Model):
    _name = "custom.serial.number"

    name = fields.Char()

    _sql_constraints = [('name_uniqe', 'unique (name)',
                         "Serial already exists.!")]

    serial_product_ids = fields.Many2many('analytic.sale.order.line', 'product_serial_rel', 'ser', 'pro')




