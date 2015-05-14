# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools import drop_view_if_exists
from logging import getLogger


_logger = getLogger(__name__)


class ReportModuleDetail(models.Model):
    """ Detailed information about modules

    Modules:
      module_id (ir.module.module): Parent model in delegated inheritance.
      model_ids (ir.model): models defined in this module.
      lang: (res.lang->code): language which will be used to show the report.

    """

    _name = 'report.module.detail'
    _description = u'Report module detail'

    _inherits = {'ir.module.module': 'module_id'}
    _auto = False
    _table = 'report_module_detail'

    _rec_name = 'name'
    _order = 'name ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    module_id = fields.Many2one(
        string='Module',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='ir.module.module',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    model_ids = fields.Many2many(
        string='Models',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='report.model.detail',
        compute=lambda self: self._compute_model_ids()
    )

    contribution_ids = fields.One2many(
        string='Contributions',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Information about contributions',
        comodel_name='report.module.contribution',
        inverse_name='module_id',
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
        help='Language in with report will be shown',
        size=50,
        default=None,
        translate=False,
        compute=lambda self: self._compute_lang()
    )

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    @api.depends('module_id')
    def _compute_model_ids(self):
        """ Searches the models (ir.model) defined in the module and fills the
            model_ids computed field
        """

        for record in self:
            record.env.cr.execute(record._models_query.format(record.name))
            ids = [row['res_id'] for row in record.env.cr.dictfetchall()]

            record.model_ids = record.env['report.model.detail'].browse(ids)

    @api.multi
    @api.depends('module_id')
    def _compute_lang(self):
        """ Gets the language used by the current user and sets it as `lang`
            field value
        """

        user_id = self.env['res.users'].browse(self.env.uid)

        for record in self:
            record.lang = user_id.lang

    # -------------------------- OVERWITEN METHODS ----------------------------

    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        self._sql_query = """
            SELECT
                "id" as "id",
                "id" as module_id
            FROM ir_module_module
            ORDER BY {}
        """

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query.format(self._order)
            )
        )

    # ----------------------- LONG CHARACTER STRINGS --------------------------

    _models_query = """
        SELECT
            res_id
        FROM
            ir_model_data
        WHERE
            model = 'ir.model'
        AND MODULE = '{}'
    """
