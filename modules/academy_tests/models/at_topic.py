# -*- coding: utf-8 -*-
#pylint: disable=I0011,W0212,E0611,C0103,R0903,C0111
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class AtTopic(models.Model):
    """ Topics are used to group serveral categories. IE, a topic named
    Internet could group the following categories: web pages, email, etc.

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'at.topic'
    _description = u'Topic in which several questions will be grouped'

    _rec_name = 'name'
    _order = 'name ASC'

    _inherit = ['mail.thread']

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help="Name for this topic",
        size=50,
        translate=True,
        track_visibility='onchange'
    )

    description = fields.Text(
        string='Description',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Something about this test',
        translate=True
    )

    at_category_ids = fields.One2many(
        string='Categories',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Allowed categories for questions in this topic',
        comodel_name='at.category',
        inverse_name='at_topic_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    # --------------------------- SQL_CONTRAINTS ------------------------------

    _sql_constraints = [
        (
            'category_uniq',
            'UNIQUE(name)',
            _(u'There are already another topic with the same name')
        )
    ]

