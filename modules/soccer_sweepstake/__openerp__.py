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
    'name': 'Soccer sweepstake',
    'summary': 'Soccer Sweepstake Project',
    'version': '1.0',

    'description': """
Soccer Sweepstake Project.
==============================================

This module allows to create and manage betting on football results inside
Odoo.

Features:
---------------------------------------------------------------------
    * Most popular leagues are included.
    * You can add your own custom leagues.
    * Most popular soccer teams are included.
    * You can add your own custom soccer teams.
    * You can create and manage seasons.
    * You can manage days of league.
    * You can manage league matches.
""",

    'author': 'Jorge Soto Garcia',
    'maintainer': 'Jorge Soto Garcia',
    'contributors': ['Jorge Soto Garcia <sotogarcia@gmail.com>'],

    'website': 'http://www.gitlab.com/sotogarcia',

    'license': 'AGPL-3',
    'category': 'Uncategorized',

    'depends': [
        'base',
        'mail'
    ],
    'external_dependencies': {
        'python': [
        ],
    },

    'data': [
        'data/soccer_league_template.xml',
        'data/soccer_team.xml',
        'data/soccer_season.xml',
        'data/soccer_league.xml',

        'security/res_groups.xml',
        'security/ir_model_access.xml',
        'security/ir_rule.xml',

        'views/ir_ui_menu.xml',
        'views/soccer_league_template.xml',
        'views/soccer_team.xml',
        'views/soccer_season.xml',
        'views/soccer_league.xml',
        'views/soccer_match.xml'

    ],
    'demo': [
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
