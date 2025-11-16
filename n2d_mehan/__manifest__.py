# -*- coding: utf-8 -*-
{
    'name': "N2D Mehan",

    'summary': """
        N2D Mehan""",

    'description': """
        N2D Mehan
    """,

    'author': "Saad Wardany",
    'license': "AGPL-3",
    'version': '0.1',

    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/data.xml',
        'views/deceased_info_views.xml',
        'views/mehan_jobs_views.xml',
        'views/mehan_work_places_views.xml',
        'views/mehan_expense_views.xml',
        'views/mehan_committee_views.xml',
        'views/mehan_relationships_age_views.xml',
        'views/mehan_bank_views.xml',
        'views/order_payment_views.xml',
        'views/beneficairies_views.xml',
        'views/injuries_classification_views.xml',
        'reports/report_action_call.xml',
        'reports/order_payment_report_print.xml',
        'reports/beneficairies_views_report.xml',
        'views/beneficiary_disbursement_permission.xml',
        'reports/beneficiary_disbursement_permission_report.xml',
        'views/report_wizard_view.xml',
        'reports/report_template.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'n2d_mehan/static/src/css/rtl.css'
        ]
    },
}
