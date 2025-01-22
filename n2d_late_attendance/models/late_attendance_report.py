from odoo import models, fields


class LateAttendanceReport(models.Model):
    _name = "late.attendance.report"

    employee_id = fields.Many2one('hr.employee', "Employee")
    check_in_date = fields.Float("Check In")
    check_out_date = fields.Float("Check Out")
    rule = fields.Many2one('late.attendance.rule', "Rule")
