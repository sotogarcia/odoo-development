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
    'name': 'Development Tools',
    'summary': 'Useful tools to make development easier OpenERP',
    'version': '1.0',

    'description': """
Development tools
==============================================

A small set of useful tools to analyze the Odoo behavior and make easy the
Odoo module development.

Included components:
---------------------------------------------------------------------
    * Domain tester.
    * Groups implied pivot table.
    * Users by group pivot table.
    * Model acess by group pivot table.

    """,

    'author': 'Jorge Soto Garcia',
    'maintainer': 'Jorge Soto Garcia',
    'contributors': ['Jorge Soto Garcia <sotogarcia@gmail.com>'],

    'website': 'http://www.gitlab.com/sotogarcia',

    'license': 'AGPL-3',
    'category': 'Technical Settings',

    'depends': [
        'base',
        'base_action_rule',
        'mail'
    ],
    'external_dependencies': {
        'python': [
        ],
    },

    'data': [
        'data/ir_actions_server.xml',
        'data/ir_values.xml',
        'data/report_paperformat.xml',
        'data/ir_filters.xml',

        'security/ir_model_access.xml',

        'demo/ir_module_category.xml',
        'demo/res_groups.xml',
        'demo/ir_filters.xml',

        'views/assets_backend.xml',
        'views/ir_ui_menu.xml',
        'views/report_groups_implied.xml',
        'views/report_groups_users.xml',
        'views/report_groups_models.xml',
        'views/base_view_view_tree.xml',
        'views/base_ir_module_module.xml',

        'wizard/dev_domain_tester.xml',
        'wizard/dev_code_tester.xml',
        'wizard/development_tools_config_settings.xml',

        'report/report_module_details.xml',
        'report/report_model_details.xml',
        'report/report_field_details.xml'
    ],
    'demo': [
        'demo/ir_module_category.xml',
        'demo/res_groups.xml',
        'demo/ir_filters.xml',
    ],
    'js': [
        'static/src/js/base_views.js'
    ],
    'css': [
        'static/src/css/styles-backend.css'
    ],
    'qweb': [
        'static/src/xml/base_base.xml',
    ],
    'images': [
    ],

    'test': [
    ],

    'installable': True
}
