# -*- coding: utf-8 -*-

from openerp import models, fields, api
from openerp.tools import drop_view_if_exists


class ReportGroupsImplied(models.Model):
    """ Model used to cross the group inheritance data in pivot tables

        This is a non auto-created model which builds a database view named
        report_groups_implied it will be used as origin of the model. The SQL
        query is defined below an entire code.
    """

    _name = 'report.groups.implied'
    _description = 'Group inheritance data to be used in pivot reports'

    _auto = False
    _table = 'report_groups_implied'

    _rec_name = 'id'
    _order = "group_name ASC, implied_name ASC"

    # ---------------------------- ENTITY  FIELDS ----------------------------

    group_id = fields.Integer(
        string='Group ID',
        required=False,
        readonly=True,
        help='Database identifier of the child group'
    )

    group_name = fields.Char(
        string='Group Name',
        required=False,
        readonly=True,
        translate=True,
        help='Name of the child group'
    )

    group_category_id = fields.Many2one(
        string='Group category',
        required=False,
        readonly=True,
        comodel_name='ir.module.category',
        help='Category to which child group belongs'
    )

    group_category_fully_qualified_xml_id = fields.Char(
        string='Group category fully qualified external ID',
        required=False,
        readonly=True,
        help=('Fully qualified external Key/Identifier of the child group '
              'category'),
    )

    group_module_id = fields.Many2one(
        string='Group module',
        required=False,
        readonly=True,
        comodel_name='ir.module.module',
        help='Module in which child group was defined'
    )

    group_module_xml_id = fields.Char(
        string='Group module external ID',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=('External Key/Identifier of the module in which the '
              'child group was defined')
    )

    group_xml_id = fields.Char(
        string='Group external ID',
        required=False,
        readonly=True,
        translate=False,
        help=('Child group external Key/Identifier that can be used for '
              'data integration with third-party systems')
    )

    group_fully_qualified_xml_id = fields.Char(
        string='Group fully qualified external ID',
        required=False,
        readonly=True,
        help='Fully qualified external Key/Identifier of the implied group'
    )

    implied_id = fields.Integer(
        string='Implied ID',
        required=False,
        readonly=True,
        help='Database identifier of the implied group'
    )

    implied_name = fields.Char(
        string='Implied Name',
        required=False,
        readonly=True,
        translate=True,
        help='Name of the implied group'
    )

    implied_category_id = fields.Many2one(
        string='Implied category',
        required=False,
        readonly=True,
        comodel_name='ir.module.category',
        help='Category to which implied group belongs'
    )

    implied_category_fully_qualified_xml_id = fields.Char(
        string='Implied category fully qualified external ID',
        required=False,
        readonly=True,
        help=('Fully qualified external Key/Identifier of the implied group '
              'category'),
    )

    implied_module_id = fields.Many2one(
        string='Implied module',
        required=False,
        readonly=True,
        comodel_name='ir.module.module',
        help='Module in which implied group was defined'
    )

    implied_module_xml_id = fields.Char(
        string='Implied module external ID',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help=('External Key/Identifier of the module in which the implied '
              'group was defined')
    )

    implied_xml_id = fields.Char(
        string='Implied external ID',
        required=False,
        readonly=True,
        translate=False,
        help=('Implied group external Key/Identifier that can be used for '
              'data integration with third-party systems')
    )

    implied_fully_qualified_xml_id = fields.Char(
        string='Implied fully qualified external ID',
        required=False,
        readonly=True,
        help='Fully qualified external Key/Identifier of the implied group'
    )

    involving_itself = fields.Boolean(
        string='Implied is itself',
        required=False,
        readonly=True,
        help='Determines when group is involving itself',
    )

    present = fields.Integer(
        string='Present',
        required=False,
        readonly=True,
        help='It\'s used to count implied groups in pivot tables'
    )

    # ------------------------- OVERWRITTEN METHODS  -------------------------

    @api.model_cr
    def init(self):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        drop_view_if_exists(self._cr, self._table)
        self._cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )

    # ------------------------- LONG TEXT CONSTANTS  -------------------------

    _sql_query = """
        WITH model_data AS (
            SELECT
                ir_model_data."name" as res_name,
                ir_model_data.res_id as res_id,
                ir_module_module."id" AS module_id,
                ir_model_data."module" as module_name
            FROM
                ir_model_data
            INNER JOIN ir_module_module
                ON ir_model_data."module" = ir_module_module.name
            WHERE
                model = 'res.groups'
        ) SELECT
            ROW_NUMBER() OVER() AS "id",
            group_info."id" AS group_id,
            group_info."name" AS group_name,
            group_info.category_id AS group_category_id,
            CASE WHEN group_cat_data."module" IS NOT NULL THEN
                CONCAT(group_cat_data."module", '.', group_cat_data."name")
            ELSE
                NULL
            END AS group_category_fully_qualified_xml_id,
            group_data."module_id" AS group_module_id,
            group_data."module_name" AS group_module_xml_id,
            group_data."res_name" as group_xml_id,
            CASE WHEN group_data."module_name" IS NOT NULL THEN
                CONCAT(group_data."module_name", '.', group_data."res_name")
            ELSE
                NULL
            END AS group_fully_qualified_xml_id,
            implied_info."id" AS implied_id,
            implied_info."name" AS implied_name,
            implied_info.category_id AS implied_category_id,
            CASE WHEN implied_cat_data."module" IS NOT NULL THEN
                CONCAT(implied_cat_data."module", '.', implied_cat_data."name")
            ELSE
                NULL
            END AS implied_category_fully_qualified_xml_id,
            implied_data."module_id" AS implied_module_id,
            implied_data."module_name" AS implied_module_xml_id,
            implied_data."res_name" as implied_xml_id,
            CASE WHEN implied_data."module_name" IS NOT NULL THEN
                CONCAT(implied_data."module_name", '.', implied_data."res_name")
            ELSE
                NULL
            END AS implied_fully_qualified_xml_id,
            group_id = implied_id AS involving_itself,
            1 AS present
        FROM (
            WITH RECURSIVE group_tree AS (
                WITH group_dependencies AS (
                    SELECT
                        res_groups."id" AS group_id,
                        res_groups_implied_rel."hid" AS implied_id
                    FROM
                        res_groups
                    LEFT JOIN res_groups_implied_rel
                        ON res_groups."id" = res_groups_implied_rel.gid
                ) SELECT
                    group_id,
                    implied_id
                FROM
                    group_dependencies
                UNION ALL
                    SELECT
                        gd.group_id,
                        gt.implied_id
                    FROM
                        group_dependencies AS gd
                    INNER JOIN group_tree AS gt
                        ON (gd.implied_id = gt.group_id)
            ) SELECT DISTINCT ON (group_id, implied_id)
                group_id,
                CASE WHEN implied_id IS NULL
                    THEN
                        group_id
                    ELSE
                        implied_id
                END AS implied_id
            FROM
                group_tree
        ) AS all_implied
        INNER JOIN res_groups as group_info
            ON group_info."id" = all_implied.group_id
        LEFT JOIN res_groups as implied_info
            ON implied_info."id" = all_implied.implied_id
        LEFT JOIN model_data as group_data
            ON group_data.res_id = all_implied.group_id
        LEFT JOIN model_data AS implied_data
            ON implied_data.res_id = all_implied.implied_id
        LEFT JOIN (
            SELECT * FROM ir_model_data WHERE model = 'ir.module.category'
        ) AS group_cat_data
            ON group_cat_data.res_id = group_info.category_id
        LEFT JOIN (
            SELECT * FROM ir_model_data WHERE model = 'ir.module.category'
        ) AS implied_cat_data
            ON implied_cat_data.res_id = implied_info.category_id
    """
