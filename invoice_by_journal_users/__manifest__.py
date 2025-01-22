# -*- coding: utf-8 -*-
# Part of Sananaz Mansuri See LICENSE file for full copyright and licensing details.

{
    'name': 'Journal Restricted Users',
    'version': '9.2.2',
    'category': 'Accounting',
    'price': 35.0,
    'currency': 'EUR',
    'summary': """Account Journal Restriction by Users""",
    'description': """
Journal Restricted Users
Account Journal Restriction by Users
    """,
    'depends': [
        'account',
    ],
    'images': ['static/description/image.png'],
    'live_test_url': 'https://probuseappdemo.com/probuse_apps/invoice_by_journal_users/235',#'https://youtu.be/MLo-B1PkwSI',
    'license': 'Other proprietary',
    'author': "Probuse Consulting Service Pvt. Ltd.",
    'website': "http://www.probuse.com",
    'support': 'contact@probuse.com',
    'data': [
        'security/account_journal_security.xml',
        'views/account_journal_view.xml',
    ],
    'qweb': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
