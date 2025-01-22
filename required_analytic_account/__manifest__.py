# -*- coding: utf-8 -*-
{
    'name': "Required analytic account",

    'summary': """
        Required analytic account""",

    'description': """
        Required analytic account
    """,

    'author': "Saad Wardany",
    'website': "http://www.yourcompany.com",
    'category': 'Account',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['account', 'sale', 'purchase'],

    # always loaded
    'data': [
        'views/views.xml',

    ],
}
