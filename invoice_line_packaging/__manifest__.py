# -*- encoding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Invoice Line Packaging',
    'version': '15.0.0',
    'author': 'Saad Wardany',
    'category': 'Accounting',
    'description': """
    Ar_En Invoice
""",
    'license': 'LGPL-3',
    'depends': ['account', 'sale'],
    'data': [
        'views/account_move_inherit.xml',
    ],
}
