from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class LateAttendanceRule(models.Model):
    _name = "late.attendance.rule"

    name = fields.Char("Name", required=True)
    start = fields.Float("Start")
    end = fields.Float("End")
    penalty = fields.Float("Penalty In Days")
    no_of_times = fields.Integer("No. of Times")
    state = fields.Selection([('draft', 'Draft'), ('confirmed', 'Confirm')], default='draft')
    active = fields.Boolean("Active", default=True)

    def action_confirm(self):
        for rec in self:
            rec.state = 'confirmed'

    @api.constrains('no_of_times')
    def _check_something(self):
        for record in self:
            if record.no_of_times <= 0:
                raise ValidationError("No. of Times must be More than 0 : %s" % record.no_of_times)
