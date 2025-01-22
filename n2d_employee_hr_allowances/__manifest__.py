# -*- coding: utf-8 -*-
{
    'name': "Employee HR Allowances",

    'summary': """
        Allowance In Contract""",

    'description': """
        Allowance In Contract
    """,

    'author': "Hossam Hassan",
    'website': "https://ivalue-s.com",
    'email': "info@ivalue-s.com",
    'license': "AGPL-3",
    'category': 'Hr',
    'version': '0.1',

    'depends': ['base', 'hr', 'hr_contract','hr_payroll_community'],
    'data': [
        'views/views.xml',
        'views/hr_employee_inherit.xml',
        'data/data.xml',
    ],
    'images': ['static/description/Banner.png'],
}
