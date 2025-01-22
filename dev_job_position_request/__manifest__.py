# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015 DevIntelle Consulting Service Pvt.Ltd (<http://www.devintellecs.com>).
#
#    For Module Support : devintelle@gmail.com  or Skype : devintelle
#
##############################################################################

{
    'name': 'Employee Request Job Position Workflow, Job Request Workflow, Job Postion Request approval Process',
    'version': '1.0',
    'sequence': 1,
    'category': 'Generic Modules/Human Resources',
    'description':
        """
        This Module add below functionality into odoo

        1.Anyone can send request for creating new job position\n
        2.New job position will be created once hr confirms it\n

Odoo app helps an employee can Request for Job Positions, employee job position, employee job request, employee job position request, job position request, request-job position by an employeen

    """,
    'summary': 'Odoo app helps an employee can Request for Job Positions, employee job position, employee job request, employee job position request, job position request, request-job position by an employee',
    'depends': ['hr_recruitment', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/template_user_to_manger_views.xml',
        'data/template_manger_to_user_views.xml',
        'data/template_job_position_rejected_views.xml',
        'views/job_position_request_sequence_views.xml',
        'views/job_position_request_views.xml',
        ],
    'demo': [],
    'test': [],
    'css': [],
    'qweb': [],
    'js': [],
    'images': ['images/main_screenshot.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
    
    # author and support Details =============#
    'author': 'DevIntelle Consulting Service Pvt.Ltd',
    'website': 'http://www.devintellecs.com',    
    'maintainer': 'DevIntelle Consulting Service Pvt.Ltd', 
    'support': 'devintelle@gmail.com',
    'price':14.0,
    'currency':'EUR',
    #'live_test_url':'https://youtu.be/A5kEBboAh_k',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
