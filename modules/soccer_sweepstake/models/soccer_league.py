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

    _sql_constraints = [
        (
            'code_company_uniq',
            'unique (template_id, season_id)',
            _(u'League already registered for this season')
        )
    ]

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
            country_id = user_set.company_id.country_id
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

    def _default_season_id(self):
        """ Gets default season, it will be the first season currently active

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
        for record in self:
            record.display_name = record._get_display_name()

    @api.model
    def _search_display_name(self, operator, value):

        domain = []

        if value:
            parts = re.split(r'[\(\)]', value)
            if parts:
                length = len(parts)
                if length > 0:
                    t_ids = self._get_ids_by_name('soccer.league.template', parts[0])
                    if t_ids:
                        domain.append(('template_id', 'in', t_ids))

                if length > 1:
                    s_ids = self._get_ids_by_name('soccer.season', parts[1])
                    if s_ids:
                        domain.append(('season_id', 'in', s_ids))

        _logger.warning("""
            value: {}
            domain: {}
            """.format(value, domain))

        return domain

    def _get_display_name(self):
        """ Gets the name for league, it will consist in name from template
            followed by season name in brackets.
        """

        self.ensure_one()

        s_name = self.season_id.shortdesc if self.season_id else ''
        t_name = self.template_id.name if self.template_id else ''

        return u'{} ({})'.format(t_name, s_name) if t_name and s_name else None

    def _get_ids_by_name(self, model_name, name):
        model_domain = [('name', '=', name)]
        model_obj = self.env[model_name]
        model_set = model_obj.search(model_domain)

        return [model.id for model in model_set]
