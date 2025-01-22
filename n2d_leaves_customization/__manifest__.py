# -*- coding: utf-8 -*-
{
    'name': "HR Leaves Customization",

    'summary': """ HR Leaves Customization """,

    'description': """  """,

    'author': "Hossam Hassan",

    'category': 'HR',

    'version': '0.1',

    'depends': ['base','hr','hr_holidays'],

    'images':[],

    # always loaded
    'data': [
        'views/hr_employee_inherit.xml',
        'views/hr_leave_type_inherit.xml'
    ],
}
