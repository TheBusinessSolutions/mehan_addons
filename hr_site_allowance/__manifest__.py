# -*- coding: utf-8 -*-
{
    'name': "HR site allowance",

    'summary': """
        HR site allowance""",

    'description': """
        HR site allowance
    """,

    'author': "Saad Wardany",
    'license': "AGPL-3",
    'category': 'Hr',
    'version': '0.1',

    'depends': ['base', 'hr_payroll_community', 'hr_attendance', 'hr_attendance_geolocation'],
    'data': [
        'security/ir.model.access.csv',
        'data/data.xml',
        'views/views.xml',
        'wizards/site_allowance_wizard.xml',
        'reports/employee_site_report.xml',
    ],
}
