# -*-coding: utf-8 -*-
{
    'name': "N2D Purchase Request",
    'author': "Hossam Hassan",
    'version': '11.0.0',

    'depends': ['sale_management', 'purchase', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_inherit.xml',
        'views/purchase_order_inherit.xml',
        'wizard/purchase_order_view.xml',

    ],
    'demo': [],
    'installable': True,
    "active": True,
    "installable": True
}
