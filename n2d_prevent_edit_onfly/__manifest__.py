# -*- encoding: utf-8 -*-
{
    "name": "N2D Prevent Edit Onfly",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "depends": [
        'base',
        'account',
        'automatic_payroll',
        'sale_management',
        'hr_contract',
        'purchase'
    ],
    "data": [
        'views/account_invoice_inherit.xml',
        'views/hr_payroll_inherit.xml',
        'views/purchase_order_inherit.xml',
        'views/sale_order_inherit.xml',
        'views/hr_contract_inherit.xml',
    ],
}
