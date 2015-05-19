# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class SoccerTeam(models.Model):
    """ Team can be usedin soccer sweepstakes

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'soccer.team'
    _description = u'Soccer team'

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

    kind = fields.Selection(
        string='Kind',
        required=False,
        readonly=False,
        index=False,
        default='CT',
        help='Type of the team',
        selection=[('CT', 'Club'), ('NT', 'National')]
    )

    country_id = fields.Many2one(
        string='Country',
        required=False,
        readonly=False,
        index=True,
        default=lambda self: self._default_country_id(),
        help='Country of the team',
        comodel_name='res.country',
        domain=[],
        context={},
        ondelete='restrict'
    )

    league_ids = fields.Many2many(
        string='Leagues',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Leagues in which this team plays',
        comodel_name='soccer.league',
        #relation='soccer_league_this_model_rel',
        #column1='soccer_league_id}',
        #column2='this_model_id',
        domain=[],
        context={},
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

