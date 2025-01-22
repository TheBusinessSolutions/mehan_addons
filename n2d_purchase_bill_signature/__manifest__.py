# -*- encoding: utf-8 -*-

{
    "name": "Net2DO Invoicing Purchase",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "Accounting",
    "depends": [
        'base',
        'account',
        'purchase'
    ],
    "data": [
        'reports/signature_layout.xml',
        'reports/po_signature_layout.xml',
        'reports/account_invoice_template.xml',
        'reports/purchase_template.xml',

    ],
    "installable": True
}
