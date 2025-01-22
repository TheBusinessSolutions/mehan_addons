# -*- encoding: utf-8 -*-

{
    "name": "Party Management System",
    "version": "1.0",
    "author": "Ahmed Hassan, Hossam Hassan",
    "license": "AGPL-3",
    "category": "Accounting",
    "depends": [
        'base',
        'sale_management',
        'sale_stock',
    ],
    "data": [
        'security/ir.model.access.csv',
        'security/sale_order_security.xml',
        'reports/account_invoice_report.xml',
        'views/sale_order_inherit.xml',
        'views/account_invoice_inherit.xml',

    ],
}
