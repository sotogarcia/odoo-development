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


class AtAlternativeWording(models.Model):
    """ Alternative wording for questions and answers

    Fields:
      name (Char): Human readable name which will identify each record.

    """

    _name = 'at.alternative.wording'
    _description = u'At alternative wording for questions and answers'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=False,
        index=True,
        default=None,
        help='Alternative wording for questions and answers',
        size=250,
        translate=True
    )

    sequence = fields.Integer(
        string='Sequence',
        required=True,
        readonly=False,
        index=False,
        default=10,
        help='Place of this alternative in the order of the alternatives'
    )

    model = fields.Selection(
        string='Model',
        required=True,
        readonly=False,
        index=False,
        default='at.question',
        help=False,
        selection=[('at.question', 'Question'), ('at.answer', 'Answer')]
    )

    res_id = fields.Integer(
        string='Resource identifier',
        required=True,
        readonly=True,
        index=False,
        default=0,
        help='Identifier of the resource to which this text can be applied'
    )
