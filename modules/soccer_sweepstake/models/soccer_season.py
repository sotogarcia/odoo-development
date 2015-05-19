# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger

from dateutil.relativedelta import relativedelta
from datetime import datetime

_logger = getLogger(__name__)


class SoccerSeason(models.Model):
    """ Season of soccer

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'soccer.season'
    _description = u'Soccer season'

    _inherit = ['mail.thread']

    _rec_name = 'shortdesc'
    _order = 'shortdesc ASC'

    shortdesc = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=lambda self: self._default_name(),
        help='Name of the season',
        size=50,
        translate=True,
        track_visibility='onchange'
    )

    begin_date = fields.Date(
        string='Begin',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._default_date(False),
        help='Date in which season will begin'
    )

    end_date = fields.Date(
        string='End',
        required=True,
        readonly=False,
        index=False,
        default=lambda self: self._default_date(True),
        help='Date in which season will end'
    )

    league_ids = fields.One2many(
        string='League',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Leagues in this season',
        comodel_name='soccer.league',
        inverse_name='season_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    def _default_name(self):
        """ Returns the default name for season, ex: 'Season 2014-2015'

            :return (unicode): default name for season
        """

        today = datetime.today()

        return u'{} {}-{}'.format(_(u'Season'), today.year - 1, today.year)

    def _default_date(self, end=False):
        """ Returns the default date for each of the season bounds

            :param end (boolean): True if end date is required False otherwise
            :return (unicode): date as unicode string
        """

        today = datetime.today()

        if end:
            result = today.strftime(u'%Y-07-31')
        else:
            result = (today - relativedelta(years=1)).strftime(u'%Y-08-01')

        return result
