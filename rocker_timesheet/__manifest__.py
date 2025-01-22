# -*- coding: utf-8 -*-
#
#############################################################################
#
#    Copyright (C) 2021-Antti Kärki.
#    Author: Antti Kärki.
#    email: antti.rocker.karki@outlook.com

#    You can modify it under the terms of the GNU AFFERO
#    GENERAL PUBLIC LICENSE (AGPL v3), Version 3.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU AFFERO GENERAL PUBLIC LICENSE (AGPL v3) for more details.
#
#    You should have received a copy of the GNU AFFERO GENERAL PUBLIC LICENSE
#    (AGPL v3) along with this program.
#    If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################


{
    'name': 'Rocker Timesheet',
    'summary': 'hr_timesheet supercharged',
    'description': 'Probably most fastest way to report work done',
    'author': 'Antti Kärki',
    'license': 'AGPL-3',
    'version': '15.0.4.0',
    'category': 'Rocker/Timesheet',
    'sequence': 23,
    'website': '',
    'depends': ['base', 'project', 'hr_timesheet', 'hr_holidays'],
    'data': [
        'security/rocker_timesheet_security.xml',
        'security/ir.model.access.csv',
        # 'views/rocker_template.xml',   # not needed in Odoo 15
        'views/rocker_timesheet_views.xml',
        'views/rocker_timesheet_about.xml',
        'views/rocker_holidays.xml',
        'views/rocker_leave_type.xml',
        'report/rocker_timesheet_report_view.xml',
    ],
    # 'demo': [
    #     # 'data/rocker_timesheet_demo.xml',
    # ],
    # Odoo 15
    'assets': {
        'web.assets_backend': [
            'rocker_timesheet/static/src/scss/rocker_calendar_button.scss',
            'rocker_timesheet/static/src/js/rocker_calendar_button.js',
            'rocker_timesheet/static/src/scss/rocker_roller_button.scss',
            'rocker_timesheet/static/src/js/rocker_roller_button.js',
            'rocker_timesheet/static/src/scss/rocker_tree_button.scss',
            'rocker_timesheet/static/src/js/rocker_tree_button.js',
        ],
        # 'web.assets_frontend': [
        #     'account/static/src/js/account_portal_sidebar.js',
        # ],
        'web.assets_qweb': [
            'rocker_timesheet/static/src/xml/**/*',
        ],

    },
    #  odoo 14
    # 'qweb': [
    #     'static/src/xml/rocker_button.xml',
    # ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'images': ['static/description/main_screenshot.gif'],

}
