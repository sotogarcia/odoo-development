# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger

import re


_logger = getLogger(__name__)


class SoccerLeague(models.Model):
    """ League of the soccer

    Fields:
        template_id (soccer.league.template): parent model
        season_id (soccer.season): parent model
        team_ids (soccer.team): parcicipan teams in the league
        display_name (char): name of the league
    """

    _name = 'soccer.league'
    _description = u'Soccer league'

    _inherit = ['mail.thread']

    _inherits = {
        'soccer.league.template': 'template_id',
        'soccer.season': 'season_id'
    }

    _rec_name = 'display_name'
    _order = 'id ASC'

    # ------------------------ DELEGATE INHERITANCE ---------------------------

    template_id = fields.Many2one(
        string='League template',
        required=True,
        readonly=False,
        index=True,
        default=lambda self: self._default_template_id(),
        help='Template on which it is based',
        comodel_name='soccer.league.template',
        domain=[],
        context={},
        ondelete='restrict',
    )

    season_id = fields.Many2one(
        string='Season',
        required=True,
        readonly=False,
        index=True,
        default=lambda self: self._default_season_id(),
        help='Season in which it is disputed',
        comodel_name='soccer.season',
        domain=[],
        context={},
        ondelete='restrict',
    )

    # ---------------------------- ENTITY FIELDS ------------------------------

    team_ids = fields.Many2many(
        string='Teams',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Teams which will play in this league',
        comodel_name='soccer.team',
        relation='soccer_league_soccer_team_rel',
        column1='soccer_league_id',
        column2='soccer_team_id',
        domain=[],
        context={},
        limit=None
    )

    # -------------------------- MANAGEMENT FIELDS ----------------------------

    display_name = fields.Char(
        string='Name',
        required=False,
        readonly=True,
        index=True,
        compute=lambda self: self._compute_display_name(),
        search=lambda self, oper, val: self._search_display_name(oper, val),
        help=False,
        size=50,
        translate=True,
        store=False
    )

    # --------------------------- SQL CONSTRAINTS -----------------------------

    _sql_constraints = [
        (
            'template_season_uniq',
            'unique (template_id, season_id)',
            _(u'League already registered for this season')
        )
    ]

    # --------------------------- FIELD FUNCTIONS -----------------------------

    def _default_template_id(self):
        """ Gets default league template, it will be the first league played in
            the country of the current user/company

            return: soccer.league.template->id or None
        """

        result = None

        # STEP 1: Getting current user and ensure one
        user_obj = self.env['res.users']
        user_set = user_obj.browse(self.env.uid)

        user_set.ensure_one()

        # STEP 2: Getting country from user (first) or company (alternative)
        if user_set.country_id:
            country_id = user_set.country_id
        elif user_set.company_id:
            country_id = user_set.company_id.country_id  # Empty allowed
        else:
            country_id = None

        # STEP 3: Getting first league from country
        if country_id:
            template_domain = [('country_id', '=', country_id.id)]
            template_obj = self.env['soccer.league.template']
            template_set = template_obj.search(template_domain, limit=1)

            if template_set:
                result = template_set.id

        return result

    @api.onchange('template_id')
    def _onchange_template_id(self):
        domain = []

        if self.template_id:
            if self.template_id.kind == 'NLC':
                if self.template_id.country_id:
                    _id = self.template_id.country_id.id
                    domain = [('country_id', '=', _id)]
                else:
                    domain = [('country_id', '!=', False)]
            else:
                domain = [('country_id', '=', False)]

        return {
            'domain': {
                'team_ids': domain
            }
        }

    def _default_season_id(self):
        """ Gets default season, it will be the first season currently active
            (begin_date <= today <= end_date)

            return: soccer.season->id or None
        """

        today = fields.Date.today()

        season_domain = [
            '&',
            ('begin_date', '<=', today),
            ('end_date', '>=', today)
        ]
        season_obj = self.env['soccer.season']
        season_set = season_obj.search(season_domain, limit=1)

        return season_set.id if season_set else None

    @api.multi
    @api.depends('season_id', 'template_id')
    def _compute_display_name(self):
        """ Computes the value for display name field
        """

        for record in self:
            s_name = record.season_id.shortdesc if record.season_id else None
            t_name = record.template_id.name if record.template_id else None

            if t_name and s_name:
                record.display_name = u'{} ({})'.format(t_name, s_name)
            else:
                record.display_name = None

    @api.model
    def _search_display_name(self, operator, value):
        """ Splits the display name to build a valid domain using original
            name (soccer.league.template)and shortdesc (soccer.season) fields
        """

        domain = []

        # STEP 1: Split display name in parts using '(' as separator
        try:
            parts = re.split(r'[\(\)]', value)  # TODO try with value.split
        except Exception as ex:
            msg_f = _(u'Search error ({}, {}). System has said: {}')
            self._log(2, msg_f, 'display_name', 'value', ex)
        else:
            length = len(parts)

        # - STEP 2: if field has two parts, & and the second test are added
            if length > 1 and parts[1]:
                domain.append('&')
                text = u'%{}%'.format(parts[1])
                domain.append(('shortdesc', 'ilike', text))

        # - STEP 3: if field has at least one part, the first test is added
            if length > 0 and parts[0]:
                text = u'%{}%'.format(parts[0])
                domain.append(('name', 'ilike', text))

        return domain

    # ------------------------- AUXILIARY FUNCTIONS ---------------------------

    def _log(self, level, msg_format, *args, **kwargs):
        """ Outputs an formated string in log

            :param level (int): 1=> debug, 2=> info, 3=> warning, 4=> error
            :param message (basestring): name of the message
        """

        methods = ['debug', 'info', 'warning', 'error']
        log = getattr(_logger, methods[level])

        msg = msg_format.format(*args, **kwargs)
        log(msg)
