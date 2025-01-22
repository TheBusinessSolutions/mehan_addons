# -*- coding: utf-8 -*-
{
    'name': "Payroll & Attendaance Integration",

    'summary': """ N2d Late Absence """,

    'description': """  """,

    'author': "Hossam Hassan",

    'version': '0.1',

    "depends": [
        "hr_attendance",
        'hr_payroll_community'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/late_attendance_report_view.xml',
        'views/late_attendance_rule.xml',
        'views/hr_payslip_inherit.xml',
        'views/res_settings_view.xml',
        'views/menuitems_view.xml',
    ],
}
