{
    'name': 'Invoice Retention Management',
    'category': 'Accounting',
    'version': '14.0.1.0',
    'summary': """Invoice Retention Management.""",
    'description': """Invoice  Retention Management.""",
    'author': "McGeorge Consulting LTD.",
    'support':'info@mcgeorgeconsulting.com',
    'website': 'www.mcgeorgeconsulting.com',
    'currency': 'USD',
    'price': 50.0,
    'license': 'OPL-1',
    'images': ["static/description/banner.png"],
    'depends': ['account'],
    'data':
        [
            'security/ir.model.access.csv',
            'views/invoice_retention_view.xml',
            'views/res_config_view.xml',
            'views/res_company.xml',        
            'wizard/create_retention_invoice_view.xml',
        ],
    
    'installable': True,
    'application': False,
    'auto_install': False,
}
