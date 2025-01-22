# -*-coding: utf-8 -*-
{
    'name': "N2D Sale Category",
    'author': "Hossam Hassan",
    'version': '11.0.0',

    'depends': ['sale_management', 'product', 'purchase', 'stock', 'analytic', 'account',
                'report_xlsx', 'stock', 'stock_account'],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_line.xml',
        'views/purchase_order_inherit.xml',
        'views/analytic_account.xml',
        'views/account_invoice_inherit.xml',
        'views/res_company_inherit.xml',
        'views/stock_picking_inventory.xml',
        'views/stock_move_inherit.xml',
        # 'views/supplier_info.xml',
        'views/menu_items.xml',
        'wizard/orders_report_wizard_views.xml',
        'reports/sale_order_report.xml',
        'reports/stock_picking_report.xml',
        'reports/purchase_order_report.xml',
        # 'reports/customer_invoices_report.xml',
        'reports/invoice_single_line.xml',
        'data/orders_report.xml',
        'data/data.xml',

    ],
    'demo': [],
    'installable': True,
    "active": True,
    "installable": True
}
