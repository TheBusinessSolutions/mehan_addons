# -*- coding: utf-8 -*-
{
    'name': "N2d hr documents",

    'summary': """
        N2d hr documents""",

    'description': """
        N2d hr documents
    """,

    'author': "Saad Wardany",
    'license': "AGPL-3",
    'category': 'Hr',
    'version': '0.1',

    'depends': ['base', 'hr', 'hr_skills'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/res_config_settings_views.xml',
        'data/scheduled_resume_check.xml',

    ],
}
