# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#
#    Copyright (c) All rights reserved:
#        (c) 2014  Jorge Soto Garcia (http://www.gitlab.com/sotogarcia)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see http://www.gnu.org/licenses
#
###############################################################################
{
    'name': '{{ name }}',
    'summary': '{{ name }} Module Project',
    'version': '1.0',

    'description': """
{{ name }} Module Project.
==============================================

Allows to quickly start the development of new Odoo modules providing a full
folder structure and some common files.

Included components:
---------------------------------------------------------------------
    * Module folder tree
    * Module manifest file (__openerp__.py)
    * File to store hierarchical group categories (data/ir_module_data.xml)
    * Groups definition (security/res_groups.xml)
    * Model access rights (security/ir_access_rights.xml)
    * Resoure access rules (security/ir_rule.xml)
    * Module main menu (views/ir_ui_menu.xml)
    """,

    'author': 'Jorge Soto Garcia',
    'maintainer': 'Jorge Soto Garcia',
    'contributors': ['Jorge Soto Garcia <sotogarcia@gmail.com>'],

    'website': 'http://www.gitlab.com/sotogarcia',

    'license': 'AGPL-3',
    'category': 'Uncategorized',

    'depends': [
        'base'
    ],
    'external_dependencies': {
        'python': [
        ],
    },

    'data': [
        'data/ir_module_data.xml',
        'data/templates.xml',

        'security/res_groups.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/ir_ui_menu.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],

    'js': [
    ],
    'css': [
    ],

    'qweb': [
    ],
    'images': [
    ],

    'test': [
    ],

    'installable': True
}
