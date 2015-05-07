# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class LeagueTemplate(models.Model):
    """ Stores information about leagues

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'league.template'
    _description = u'League template'

    _inherit = ['mail.thread']

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help=False,
        size=50,
        translate=True,
        track_visibility='onchange'
    )

    country_id = fields.Many2one(
        string='Country',
        required=False,
        readonly=False,
        index=True,
        default=lambda self: self._default_country_id(),
        help='Country where the league is played',
        comodel_name='res.country',
        domain=[],
        context={},
        ondelete='restrict'
    )

    kind = fields.Selection(
        string='Kind',
        required=True,
        readonly=False,
        index=True,
        default='NLC',
        help='Type of the league',
        selection=[
            ('NLC', 'Clubs'),
            ('ILC', 'Clubs (International)'),
            ('ILN', 'Nations'),
        ]
    )

    league_ids = fields.One2many(
        string='League',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Leagues based in this template',
        comodel_name='soccer.league',
        inverse_name='template_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    def _default_country_id(self):
        """ Returns the country of the default company of the current user

            :return (res.country): country if is set or None
        """
        result = None

        user_id = self.env['res.users'].browse(self.env.uid)
        if user_id and user_id.company_id and user_id.company_id.country_id:
            result = user_id.company_id.country_id.id

        return result

    @api.one
    @api.onchange('kind')
    def _onchange_kind(self):
        if self.kind != 'NLC':
            self.country_id = None
        else:
            self.country_id = self._default_country_id()
