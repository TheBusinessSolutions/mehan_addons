# -*- encoding: utf-8 -*-

{
    "name": "N2D Attendance Management",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "HR enhancement module",
    "depends": [
        'base',
        'hr_attendance',
        'hr_payroll_community',
    ],
    "data": [
        'data/data.xml',
        'views/hr_employee_inherit.xml',
        'views/hr_attendance_inherit.xml',
        'views/hr_payslip_inherit.xml',
    ],
}
