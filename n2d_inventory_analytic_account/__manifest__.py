# -*-coding: utf-8 -*-
{
    'name': "N2D Inventory Analytic Account",
    'author': "Hossam Hassan",
    'version': '13.0.0',

    'depends': ['analytic', 'account', 'stock_account', 'purchase'],

    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_inventory.xml',
        'report/purchase_order_report.xml',
        'report/report_picking_inherit.xml',
        # 'views/stock_move_inherit.xml',
        'data/data.xml',
    ],
    'demo': [],
    'installable': True,
    "active": True,
    "installable": True
}
