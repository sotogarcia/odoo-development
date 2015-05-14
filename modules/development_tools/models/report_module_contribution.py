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


class ReportModuleContribution(models.Model):
    """ Retrieves the names and email addresses of all developers of installed
        modules

    Fields:
      name (Char): Contribution name
      email (Char): Contribution email address
      module_id (Many2one): Module in which he has contributed

    """

    _name = 'report.module.contribution'
    _description = u'Report module contribution'

    _auto = False
    _table = 'report_module_contribution'

    _rec_name = 'name'
    _order = 'name ASC'

    name = fields.Char(
        string='Name',
        required=True,
        readonly=True,
        index=True,
        default=None,
        help='Name of the contributor',
        size=50,
        translate=False
    )

    email = fields.Char(
        string='Email',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Email address of the contributor',
        size=50,
        translate=False
    )

    module_id = fields.Many2one(
        string='Module',
        required=True,
        readonly=False,
        index=False,
        default=None,
        help='Module in which he has contributed',
        comodel_name='ir.module.module',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        self._sql_query = """
            WITH contribution_lines AS (
                SELECT
                    ID,
                    UNNEST (
                        string_to_array("contributors", ',')
                    ) AS line
                FROM
                    ir_module_module
            ) SELECT
                ROW_NUMBER () OVER () AS ID,
                TRIM (
                    BOTH ' '
                    FROM
                        SUBSTRING (line, '^[^<]*')
                ) AS "name",
                TRIM (
                    BOTH ' '
                    FROM
                        regexp_replace(
                            SUBSTRING (line, '<[^>]+>'),
                            '[<>]',
                            '',
                            'g'
                        )
                ) AS "email",
                ID AS module_id
            FROM
                contribution_lines
        """

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
