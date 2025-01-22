# -*- coding: utf-8 -*-
# Part of Odoo, Aktiv Software PVT. LTD.
# See LICENSE file for full copyright & licensing details.

# Author: Aktiv Software.
# mail: odoo@aktivsoftware.com
# Copyright (C) 2015-Present Aktiv Software PVT. LTD.
# Contributions:
# Aktiv Software:
# - Mital Parmar
# - Bhavin Kanani
# - Harshil Soni

{
    'name': "Employee Automatically Leave Allocation",
    'summary': """
       """,
    'version': '15.0.1.0.0',
    'license': "AGPL-3",
    'author': "Aktiv Software",
    'website': "http://www.aktivsoftware.com",
    'category': 'Generic Modules/Human Resources',
    'description': """
        This application controls the leave schedule of your company.
        And Allocate Leaves to newly added Employee.
    """,
    'depends': [
        'hr_holidays', 'hr'
    ],

    'data': [
        'views/res_config_settings_views.xml',
        'views/hr_employee_views.xml'
    ],

    'images': [
        'static/description/banner.jpg',
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
