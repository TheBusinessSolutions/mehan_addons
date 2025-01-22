# -*- encoding: utf-8 -*-

{
    "name": "N2D HR",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "HR enhancement module",
    "depends": [
        'base',
        'hr',
        'hr_payroll_community',
        'n2d_employee_hr_allowances',
        'actions_management',

    ],
    "data": [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'data/scheduled_id_passport_check.xml',
        'views/hr_overtime_view.xml',
        'views/res_settings_view.xml',
        'views/hr_absence_view.xml',
        'views/hr_bonus_confg_view.xml',
        'views/hr_penalty_confg_view.xml',
        'views/hr_bonus_view.xml',
        'views/hr_penalty_view.xml',
        'views/menu_item_view.xml',
        'views/hr_employee_view.xml',
        'views/hr_payslip_inherit.xml',
        'reportes/payslip_report_inherit.xml',
    ],
}
