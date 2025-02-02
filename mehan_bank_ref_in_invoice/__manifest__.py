{
    'name': 'Mehan Bank Ref in Invoice',
    'version': '1.0',
    'summary': 'Display bank statement reference in the invoice payment report',
    'description': """
        This module extends the invoice report to display the bank statement reference (ref)
        from the payment's bank statement line.
    """,
    'author': 'Your Name',
    'depends': ['account'],
    'data': [
        'views/account_move_report_templates.xml',
    ],
    'installable': True,
    'application': False,
}
