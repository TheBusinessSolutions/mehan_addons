# -*-coding: utf-8 -*-
{
    'name': "General Changes",
    'author': "Saad Wardany",
    'version': '15.0.0',

    'depends': ['base','ohrms_loan','hr','ohrms_loan_accounting', 'hr_contract'],

    'data': [
        'security/ir.model.access.csv',
        'views/loan_request_form_inherit.xml',
        'views/res_config_settings_views.xml',
        'data/scheduled_contract_check.xml',
    ],
    'demo': [],
    'installable': True,
    "active": True,
    "installable": True
}
