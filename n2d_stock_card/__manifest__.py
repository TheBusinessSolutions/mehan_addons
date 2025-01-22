# -*-coding: utf-8 -*-
{
    'name': "N2D Stock card",

    'summary': "Add an report stock card in inventory",

    'description': """
        Print stock card.

        Print a stock card for a location wether it is for a internal,
        view, inventory, production or scrapped location. This module
        will give you the in, out and the balance of location between
        a period.
    """,

    'author': "HIntegration",
    'website': "https://hintegration.com/",
    'category': 'Warehouse',
    'version': '13.0.0',

    'depends': ['base', 'stock', 'web', 'account'],

    'data': [
        'security/ir.model.access.csv',

        # reports
        'reports/stock_card_report.xml',
        'reports/stock_card_details_report.xml',

        # wizards
        'wizards/stock_card_wizard_views.xml'
    ],
    'demo': [],
    'installable': True,
    'images': ['static/images/main_screenshot.png']
}
