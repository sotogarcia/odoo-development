# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api, api
from openerp.tools.translate import _
from openerp.tools import drop_view_if_exists
from logging import getLogger


_logger = getLogger(__name__)


class ReportModelDetail(models.Model):
    """ Detailed information about models

    Fields:
      model_id (ir.model): Parent model in delegated inheritance.

    """

    _name = 'report.model.detail'
    _description = u'Report model detail'

    _inherits = {'ir.model': 'model_id'}
    _auto = False
    _table = 'report_model_detail'

    _rec_name = 'name'
    _order = 'name ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    model_id = fields.Many2one(
        string='Field',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='ir.model',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    field_ids = fields.One2many(
        string='Fields',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='report.field.detail',
        inverse_name='model_id',
        domain=[],
        context={},
        auto_join=False,
        limit=None
    )

    # -------------------------- MANAGEMENT FIELDS ----------------------------

    lang = fields.Char(
        string='Language',
        required=True,
        readonly=True,
        index=False,
        help=False,
        size=50,
        translate=False,
        compute=lambda self: self._compute_lang()
    )

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    @api.depends('model_id')
    def _compute_lang(self):
        """ Gets the language used by the current user and sets it as `lang`
            field value
        """

        user_id = self.env['res.users'].browse(self.env.uid)

        for record in self:
            record.lang = user_id.lang

    # -------------------------- OVERWITEN METHODS ----------------------------

    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """
        self._sql_query = """
            SELECT
                "id" AS "id",
                "id" as model_id
            FROM ir_model
            WHERE model <> '{}'
            ORDER BY {}
        """.format(self._name, self._order)

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
