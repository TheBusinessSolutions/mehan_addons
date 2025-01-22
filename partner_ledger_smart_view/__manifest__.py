
{
    'name': 'Partner Ledger From Contact',
    'summary': 'Adds smart button to view partner ledger from contact',
    'description': '''
This module provide smart clickable button in partner through which general ledger can be viewed directly ''',
    'author': "10 Orbits",
    'website': "https://www.10orbits.com",
    'version': '15.0.1.0.0',
    'category': 'Accounting/Accounting',
    'depends': [
        'dynamic_accounts_report'
    ],
    'data': [
        'views/partner_smart_button_view.xml',
    ],
    'assets': {
       
        'web.assets_backend': [
            'partner_ledger_smart_view/static/src/js/partner_smart_button.js',
            
        ],
        
    },
    'images': ['static/description/Banner.png'],
    'installable': True,
    'application': False,
}
