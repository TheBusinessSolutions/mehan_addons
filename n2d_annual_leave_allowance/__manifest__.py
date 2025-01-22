# -*- encoding: utf-8 -*-

{
    "name": "HR Leave Allowances",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "HR enhancement module",
    "depends": [
        'base',
        'hr',
        'hr_payroll',
        'hr_holidays',
        'account',
        'n2d_hr_structure',
    ],
    "data": [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/annual_leave_allowances.xml',
        'views/res_settings_view.xml',
        'views/hr_leave_type_inherit.xml',
        'views/menu_item_views.xml',
        'views/vacation_report.xml',
        'views/annual_layout.xml',
    ],
}
