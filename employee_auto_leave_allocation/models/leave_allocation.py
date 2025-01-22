# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

from odoo import api, fields, models


class Employee(models.Model):
    """Class Inherit for adding some new leave functionality."""

    _inherit = "hr.employee"
    _description = "Employee"

    joining_date = fields.Date(string="Joining Date", default=fields.Date.context_today)

    @api.model
    def create(self, vals):
        """Method Override for allocate leaves to the employee."""
        employee = super(Employee, self).create(vals)
        conf_val = self.env['res.config.settings'].search(
            [], order='id desc', limit=1)
        for leave_obj in conf_val.holiday_status_id:
            if conf_val and conf_val.auto_leave_allocation:
                if employee.company_id.id == (conf_val.company_id.id):
                    leave_allocations = self.env['hr.leave.allocation'].search(
                        [('holiday_status_id', '=',leave_obj.id)])
                    if leave_allocations:
                        for leave_allocation in leave_allocations:
                            allocation_dict = {
                                'name': leave_allocation.name,
                                'holiday_status_id': leave_allocation.holiday_status_id.id,
                                'number_of_days': leave_allocation.number_of_days,
                                'holiday_type': 'employee',
                                'employee_id': employee.id,
                            }
                        new_allocation = self.env['hr.leave.allocation'].create(allocation_dict)
                        new_allocation.sudo().action_confirm()
        return employee
