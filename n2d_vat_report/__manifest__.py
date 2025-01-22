# -*- coding: utf-8 -*-

{
   'name': "VAT Report",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "depends": ['account', 'report_xlsx'],
   'data': [
        'security/ir.model.access.csv',
        'report/report.xml',
        'report/vat_report.xml',
        'wizard/vat_report_view.xml',
    ],
}

