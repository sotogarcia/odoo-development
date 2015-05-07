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
    """ League of soccer

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'soccer.league'
    _description = u'Soccer league'

    _inherit = ['mail.thread']

    _inherits = {
        'league.template': 'template_id',
        'soccer.season': 'season_id'
    }

    _rec_name = 'display_name'
    _order = 'id ASC'

    template_id = fields.Many2one(
        string='Template',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        comodel_name='league.template',
        domain=[],
        context={},
        ondelete='restrict',
    )

    season_id = fields.Many2one(
        string='Season',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
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
        # relation='model_name_this_model_rel',
        # column1='model_name_id}',
        # column2='this_model_id',
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

    def _get_display_name(self):
        s_name = self.season_id.name if self.season_id else ''
        t_name = self.template_id.name if self.template_id else ''

        return u'{} ({})'.format(t_name, s_name) if t_name and s_name else None

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
                    t_ids = self._get_ids_by_name('league.template', parts[0])
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

    def _get_ids_by_name(self, model_name, name):
        model_domain = [('name', '=', name)]
        model_obj = self.env[model_name]
        model_set = model_obj.search(model_domain)

        return [model.id for model in model_set]
