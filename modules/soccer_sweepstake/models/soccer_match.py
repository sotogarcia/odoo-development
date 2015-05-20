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


class SoccerMatch(models.Model):
    """ Match between two teams from the same league

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'soccer.match'
    _description = u'League match'

    _inherit = ['mail.thread']

    _rec_name = 'name'
    _order = 'match_day ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    league_id = fields.Many2one(
        string='League',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='League to which the match belongs',
        comodel_name='soccer.league',
        domain=[],
        context={},
        ondelete='cascade',
        auto_join=False
    )

    local_id = fields.Many2one(
        string='Local team',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Team playing at home',
        comodel_name='soccer.team',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    local_goals = fields.Integer(
        string='Local goals',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Goals scored by the home team'
    )

    away_id = fields.Many2one(
        string='Away team',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Team not playing at home',
        comodel_name='soccer.team',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    away_goals = fields.Integer(
        string='Away goals',
        required=True,
        readonly=False,
        index=False,
        default=0,
        help='Goals scored by the visiting team'
    )

    match_day = fields.Date(
        string='Match day',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_match_day(),
        help='Day in which the match will be played'
    )

    # -------------------------- MANAGEMENT FIELDS ----------------------------

    name = fields.Char(
        string='Name',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Name of the match',
        size=50,
        compute=lambda self: self._compute_name(),
        search=lambda self, oper, val: self._search_name(oper, val)
    )

    # --------------------------- SQL CONSTRAINTS -----------------------------

    _sql_constraints = [
        (
            'two_diferente_teams',
            'CHECK (local_id <> away_id)',
            _(u'Two diferent teams are needed for play a match')
        ),
        (
            'positive_number_of_goals',
            'CHECK (local_goals >= 0 and away_goals >= 0)',
            _(u'The number of goals must be greater or equal than zero')
        ),
    ]

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.onchange('league_id')
    def _onchange_league_id(self):
        """ When league has been changed, the domain for local and away tems
            must be changed too, new domains will allow to choose teams from
            the selected league.
        """

        self.local_id = None
        self.away_id = None

        team_ids = self._get_team_ids()
        return {
            'domain': {
                'local_id': [('id', 'in', team_ids)],
                'away_id': [('id', 'in', team_ids)]
            }
        }

    @api.multi
    @api.depends('local_id', 'away_id')
    def _compute_name(self):
        """ Compute the value for `name` field, it will be the local and away
            team names separated by a dash (long dash)
        """

        for record in self:
            record.name = self._get_name()

    @api.model
    def _search_name(self, operator, value):
        """ Builds a valid domain using ids from selected teams instead
            this computed name
        """
        domain = []

        # STEP 1: Split name in parts using '—' as separator
        try:
            parts = re.split(r'[—]', value)  # TODO try with value.split
        except Exception as ex:
            msg_f = _(u'Search error ({}, {}). System has said: {}')
            self._log(2, msg_f, 'name', 'value', ex)
        else:
            length = len(parts)

        # - STEP 2: if field has two parts, & and the second test are added
            if length > 1 and parts[1]:
                domain.append('&')

                team_domain = [('name', '=', parts[1])]
                team_obj = self.env['soccer.team']
                team_set = team_obj.search(team_domain)

                _ids = [team.id for team in team_set]
                domain.append(('away_id', 'in', _ids))

        # - STEP 3: if field has at least one part, the first test is added
            if length > 0 and parts[0]:
                team_domain = [('name', '=', parts[0])]
                team_obj = self.env['soccer.team']
                team_set = team_obj.search(team_domain)

                _ids = [team.id for team in team_set]
                domain.append(('away_id', 'in', _ids))

        return domain

    @api.onchange('local_id')
    def _onchange_local_id(self):
        """ Changes de value of the name (compited field) and removes the
            selected team from the allowed away teams.
        """

        self.name = self._get_name()

        team_ids = self._get_team_ids()
        if team_ids and self.local_id:
            team_ids.remove(self.local_id.id)
        return {
            'domain': {
                'away_id': [('id', 'in', team_ids)]
            }
        }

    @api.onchange('away_id')
    def _onchange_away_id(self):
        """ Changes de value of the name (compited field) and removes the
            selected team from the allowed local teams.
        """

        self.name = self._get_name()

        team_ids = self._get_team_ids()
        if team_ids and self.away_id:
            team_ids.remove(self.away_id.id)
        return {
            'domain': {
                'local_id': [('id', 'in', team_ids)]
            }
        }

    def _default_match_day(self):
        """ Default value for day of the match, it will be today for new
            records.
        """

        return fields.Date.context_today(self)

    # ------------------------- AUXILIARY FUNCTIONS ---------------------------

    def _get_team_ids(self):
        """ Gets the ids of the all the teams playing in choosen league
        """

        self.ensure_one()

        if self.league_id and self.league_id.team_ids:
            team_ids = [team.id for team in self.league_id.team_ids]
        else:
            team_ids = [-1]  # No teams

        return team_ids

    def _get_name(self):
        """ Builds the name (computed field) using the original names of the
            both teams separated by a (long) dash.
        """

        self.ensure_one()

        local = self.local_id
        away = self.away_id

        if local and local.name and away and away.name:
            result = u'{} — {}'.format(local.name, away.name)
        else:
            result = _(u'New match')

        return result

    def _log(self, level, msg_format, *args, **kwargs):
        """ Outputs an formated string in log

            :param level (int): 1=> debug, 2=> info, 3=> warning, 4=> error
            :param message (basestring): name of the message
        """

        methods = ['debug', 'info', 'warning', 'error']
        log = getattr(_logger, methods[level])

        msg = msg_format.format(*args, **kwargs)
        log(msg)
