# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class LeagueMatch(models.Model):
    """ Match between two teams from the same league

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'league.match'
    _description = u'League match'

    _inherit = ['mail.thread']

    _rec_name = 'name'
    _order = 'match_day ASC'

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

    match_day = fields.Date(
        string='Match day',
        required=False,
        readonly=False,
        index=False,
        default=lambda self: self._default_match_day(),
        help='Day in which the match will be played'
    )

    league_selected = fields.Boolean(
        string='League was selected',
        required=False,
        readonly=True,
        index=False,
        default=False,
        help='Check if league has been selected',
        compute=lambda self: self._compute_league_selected()
    )

    @api.onchange('league_id')
    def _onchange_league_id(self):
        self.league_selected =  bool(self.league_id)

        if self.league_id and self.league_id.team_ids:
            team_ids = [team.id for team in self.league_id.team_ids]
        else:
            team_ids = [-1]

        return {
            'domain': {
                'local_id': [('id', 'in', team_ids)],
                'away_id': [('id', 'in', team_ids)]
            }
        }

    @api.multi
    @api.depends('local_id', 'away_id')
    def _compute_name(self):
        for record in self:
            record.name = record._get_name()

    def _get_name(self):
        local = self.local_id
        away = self.away_id
        result = ''

        if local and local.name and away and away.name:
            result = u'{} — {}'.format(local.name, away.name)

        return result

    @api.model
    def _search_name(self, operator, value):

        domain = []

        if value:
            parts = re.split(r'[—]', value)
            if parts:
                length = len(parts)
                if length > 1:
                    l_ids = self._get_ids_by_name('soccer.team', parts[0])
                    a_ids = self._get_ids_by_name('soccer.team', parts[1])
                    domain.append(('local_id', 'in', l_ids))
                    domain.append(('away_id', 'in', a_ids))

        _logger.warning("""
            value: {}
            domain: {}
            """.format(value, domain))

        return domain

    def _default_match_day(self):
        return fields.Date.context_today(self)

    @api.multi
    @api.depends('league_id')
    def _compute_league_selected(self):
        for record in self:
            record.league_selected =  bool(self.league_id)


