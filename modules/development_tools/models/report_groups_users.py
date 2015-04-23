# -*- coding: utf-8 -*-

from openerp import models, fields
from openerp.tools import drop_view_if_exists


class ReportGroupsImplied(models.Model):
    """ Model used to cross the groups and their users in pivot tables

        This is a non auto-created model which builds a database view named
        report_groups_users it will be used as origin of the model. The SQL
        query is defined below an entire code.

        Model inherits all fields from report.groups.implied except id , but
        they are filled by the new SQL query from the created view.
    """
    _inherit = 'report.groups.implied'

    _name = 'report.groups.users'
    _description = ('Data of users by group (and implied) to be used in '
                    'pivot table reports')

    _auto = False
    _table = 'report_groups_users'

    _rec_name = 'id'
    _order = "group_name ASC, user_name ASC"

    # ---------------------------- ENTITY  FIELDS ----------------------------

    user_id = fields.Integer(
        string='User ID',
        required=False,
        readonly=True,
        help='User database identifier'
    )

    user_name = fields.Char(
        string='User name',
        required=False,
        readonly=True,
        help='User login name',
    )

    user_module_id = fields.Many2one(
        string='User module',
        required=False,
        readonly=True,
        comodel_name='ir.module.module',
        help='Module in which user was defined',
    )

    user_module_xml_id = fields.Char(
        string='User module external ID',
        required=False,
        readonly=True,
        help=('External Key/Identifier of the module in which user was '
              'defined')
    )

    user_xml_id = fields.Char(
        string='User external ID',
        required=False,
        readonly=True,
        help=('User external Key/Identifier that can be used for '
              'data integration with third-party systems'),
    )

    user_fully_qualified_xml_id = fields.Char(
        string='User fully qualified external ID',
        required=False,
        readonly=True,
        help='Fully qualified external Key/Identifier of the user'
    )

    # ------------------------- OVERWRITTEN METHODS  -------------------------

    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )

    # ------------------------- LONG TEXT CONSTANTS  -------------------------

    _sql_query = """
        WITH model_data AS (
            SELECT
                ir_model_data."name" AS res_name,
                ir_model_data.res_id AS res_id,
                ir_module_module."id" AS module_id,
                ir_model_data."module" AS module_name
            FROM
                ir_model_data
            INNER JOIN ir_module_module
                ON ir_model_data."module" = ir_module_module. NAME
            WHERE
                model = 'res.users'
        ) SELECT DISTINCT
            ON (user_id, group_id) --
            ROW_NUMBER () OVER () AS "id",
            --
            users."id" AS user_id,
            users."login" AS user_name,
            model_data.module_id as user_module_id,
            model_data.module_name as user_module_xml_id,
            model_data.res_name as user_xml_id,
            CASE WHEN model_data.module_name IS NOT NULL
                THEN
                    CONCAT(model_data.module_name, '.', model_data.res_name)
                ELSE
                    NULL
            END AS user_fully_qualified_xml_id,
            --
            groups.group_id,
            groups.group_name,
            groups.group_category_id,
            groups.group_category_fully_qualified_xml_id,
            groups.group_module_id,
            groups.group_module_xml_id,
            groups.group_xml_id,
            groups.group_fully_qualified_xml_id,
            groups.implied_id,
            groups.implied_name,
            groups.implied_category_id,
            groups.implied_category_fully_qualified_xml_id,
            groups.implied_module_id,
            groups.implied_module_xml_id,
            groups.implied_xml_id,
            groups.implied_fully_qualified_xml_id,
            groups.involving_itself,
            groups.present
        FROM
            report_groups_implied AS groups
        FULL JOIN res_groups_users_rel AS rel ON rel.gid = groups."implied_id"
        FULL JOIN res_users AS users ON rel.uid = users."id"
        LEFT JOIN model_data AS model_data ON model_data.res_id = users."id"
    """
