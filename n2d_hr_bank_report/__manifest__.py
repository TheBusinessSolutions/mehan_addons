# -*- encoding: utf-8 -*-

{
    'name': 'Bank Report',
    'version': '11.0.1.0.0',
    'author': 'Hossam Hassan',
    'category': '',
    'license': '',
    'depends': ['hr_payroll_community'],
    'data': [
        'security/ir.model.access.csv',
        'wizards/bank_report_wizard.xml',
        'reports/bank_report.xml',
    ],
    'installable': True,
    'auto_install': False,
}
