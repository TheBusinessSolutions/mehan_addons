# -*- coding: utf-8 -*-
{
    'name': "Is a Customer and Is a Vendor",

    'summary': """
        Add Field Is a Customer And Is a Vendor""",

    'description': """
        *   Add Field Is a Customer And Is a Vendor checkbox Into The Partner Form For Identification.\n
        *   Easy To Use.\n
        *   User Can Manually Set / Unset Customer and Vendor Checkbox.\n
        *   Add Customer Filter In Sale Order.\n
        *   Add Vendor Filter In Purchase Order.
    """,

    'license': "LGPL-3",
    'images': ['static/description/cupdev2.png'],
    'author': "Yusup Nur Karimah",
    'website': "https://yusupnurkarimah.github.io/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','account','sale_management','purchase'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
    ],
}