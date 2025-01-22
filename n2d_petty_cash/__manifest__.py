# -*- encoding: utf-8 -*-

{
    "name": "Petty Cash",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "Specific Industry Applications",
    "depends": [
        'base',
        'hr',
        'purchase',
        'stock',
        'account'
    ],
    "data": [
        'data/data.xml',
        'security/res_groups.xml',
        'security/ir.model.access.csv',
        'views/res_settings.xml',
        'views/add_cash_to_petty.xml',
        'views/reconcile.xml',
        'views/pay_from_petty.xml',
        'views/petty_cash_batch.xml',
        'views/inventory_inherit.xml',
        'views/petty_batch_report.xml',
        'views/hr_employee_inherit.xml',
        'views/petty_cash_kanban.xml'
    ],
}
