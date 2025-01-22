from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta


class HrPayslip(models.Model):
    _inherit = "hr.payslip"
    late_rule_ids = fields.Many2many('late.attendance.rule', string="Late Rules")
    late_attendace_amount = fields.Float("Late Attendance Amount")

    def compute_sheet(self):
        super(HrPayslip, self).compute_sheet()
        for rec in self:
            rec.get_late_attendance_rules()
            rec.late_attendace_amount = rec.compute_late_attendance(rec)
        return super(HrPayslip, self).compute_sheet()

    def compute_late_attendance(self, payslip):
        days = 0
        month_days = float(
            self.env['ir.config_parameter'].sudo().get_param('n2d_late_attendance.late_attendance_month_days'))
        if month_days <= 0:
            raise ValidationError("Please Set Late Attendance Month Days in Payroll Configuration!!")

        for rule in payslip.late_rule_ids:
            days += rule.penalty
        total = (days / month_days) * payslip.contract_id.wage
        return total

    def get_late_attendance_rules(self):
        for record in self:
            rules = self.env['late.attendance.rule'].search([('state', '=', 'confirmed')])
            late_time = float(
                self.env['ir.config_parameter'].sudo().get_param('n2d_late_attendance.late_attendance_time'))
            late_attend_time = late_time

            for rule in rules:
                total = 0
                attendances = self.env['hr.attendance'].search(
                    [('employee_id', '=', record.employee_id.id), ('check_in', '>=', record.date_from),
                     ('check_out', '<=', record.date_to)])
                if rule.id in record.late_rule_ids.ids:
                    continue
                else:
                    for attendance in attendances:
                        check_in = fields.Datetime.from_string(attendance.check_in) + timedelta(hours=2)
                        check_out = fields.Datetime.from_string(attendance.check_out) + timedelta(hours=2)
                        check_in_time = check_in.strftime('%H:%M')
                        check_out_time = check_out.strftime('%H:%M')
                        hour, minute = check_in_time.split(':')
                        ehour, eminute = check_out_time.split(':')
                        minute = float(minute) / 60
                        minute = str(minute).split('.')[1]
                        eminute = float(eminute) / 60
                        eminute = str(eminute).split('.')[1]
                        check_in_time = float('{}.{}'.format(hour, minute))
                        check_out_time = float('{}.{}'.format(ehour, eminute))

                        if rule.start <= check_in_time <= rule.end:
                            diff_late_in = check_in_time - rule.start

                            if diff_late_in <= late_attend_time:
                                total_diff_late_in = late_attend_time - diff_late_in

                                if total_diff_late_in < 0:
                                    total += 1
                                else:
                                    late_attend_time -= total_diff_late_in
                            else:
                                total += 1

                        if rule.start <= check_out_time <= rule.end:
                            diff_late_out = rule.end - check_out_time
                            if diff_late_out <= late_attend_time:
                                total_diff_late_out = late_attend_time - diff_late_out
                                if total_diff_late_out < 0:
                                    total += 1
                                else:
                                    late_attend_time -= total_diff_late_out
                            else:
                                total += 1

                if total > rule.no_of_times:
                    values = {
                        'employee_id': record.employee_id.id,
                        'rule': rule.id,
                        'check_in_date': rule.start,
                        'check_out_date': rule.end,
                    }

                    record.late_rule_ids += rule
                    self.env['late.attendance.report'].create(values)
