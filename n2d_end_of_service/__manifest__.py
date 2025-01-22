# -*- encoding: utf-8 -*-
{
    "name": "N2D End of Service",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "HR enhancement module",
    "depends": [
        'base',
        'hr',
        'hr_payroll',
        'n2d_leaves_customization',
        'hr_holidays',
        'n2d_employee_hr_allowances',
        'n2d_hr_structure'
    ],
    "data": [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/hr_contract_inherit.xml',
        'views/eos_reason.xml',
        'views/employee_end_of_service.xml',
        'views/res_settings_view.xml',
        'views/menuitem_view.xml',
        'views/end_of_service_layout.xml',
        'views/end_of_service_report.xml',
    ],
}
