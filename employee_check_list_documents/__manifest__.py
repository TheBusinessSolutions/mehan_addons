# -*- coding: utf-8 -*-
{
    'name': "Employee Check List",

    'summary': """
        Employee Check List""",

    'description': """
        Employee Check List
    """,

    'author': "Saad Wardany",
    'license': "AGPL-3",
    'category': 'Hr',
    'version': '0.1',

    'depends': ['base', 'hr', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/checklist_view.xml',
        'views/hr_employee_inherit.xml',
        'views/checklist_document_seq.xml',

    ],
}
