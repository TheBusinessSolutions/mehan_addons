# -*- coding: utf-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2018 BroadTech IT Solutions Pvt Ltd 
#    (<http://broadtech-innovations.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
{
    'name': 'Asset Management',
    'version': '15.0',
    'category': 'custom',
    'summary': 'Asset Management',
    'license':'LGPL-3',
    'price' : 20.0,
    'currency': 'USD',
    'description': """
     Asset management is a simple system to manage assets owned by an organization.
""",
    'author' : 'BroadTech IT Solutions Pvt Ltd',
    'website' : 'http://www.broadtech-innovations.com',
    'depends': ['base', 'mail', 'hr'],
    'images': ['static/description/banner.jpg'],
    'data': [
         'security/security.xml',
         'security/ir.model.access.csv',
         'views/asset_sequence.xml',
         'views/asset_view.xml',
         'views/asset_move_view.xml',
         'wizards/qr_code_wizard.xml',
         'reports/qr_report.xml',

    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=2:softtabstop=2:shiftwidth=2:
