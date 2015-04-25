from openerp import models, fields
from openerp import tools


class ModelName(models.Model):
    """ Model used to cross the groups and their model access in pivot tables

        This is a non auto-created model which builds a database view named
        report_groups_models it will be used as origin of the model. The SQL
        query is defined below an entire code.

        Model inherits all fields from report.groups.implied except id, but
        they are filled by the new SQL query from the created view.

    """

    _inherit = 'report.groups.implied'

    _name = 'report.groups.models'
    _description = ('Data of models by group (and implied) to be used in '
                    'pivot table reports')

    _auto = False
    _table = 'report_groups_models'

    _rec_name = 'id'
    _order = "group_name ASC, model_name ASC"

    # -----------------------------ENTITY FIELDS-------------------------------

    model_id = fields.Integer(
        string='Model ID',
        required=False,
        readonly=True,
        help='Model database identifier'
    )

    model_name = fields.Char(
        string='Model name',
        required=False,
        readonly=True,
        help='Model name (this is the ir.model.model value)',
    )

    model_module_id = fields.Many2one(
        string='Model module',
        required=False,
        readonly=True,
        comodel_name='ir.module.module',
        help='Module in which model was defined',
    )

    model_module_xml_id = fields.Char(
        string='Model module external ID',
        required=False,
        readonly=True,
        help=('External Key/Identifier of the module in which model was '
              'defined')
    )

    model_xml_id = fields.Char(
        string='Model external ID',
        required=False,
        readonly=True,
        help=('User external Key/Identifier that can be model for '
              'data integration with third-party systems'),
    )

    model_fully_qualified_xml_id = fields.Char(
        string='Model fully qualified external ID',
        required=False,
        readonly=True,
        help='Fully qualified external Key/Identifier of the model'
    )

    perm_create = fields.Boolean(
        string='Create',
        required=False,
        readonly=True,
        help="Group can create new model records"
    )

    perm_read = fields.Boolean(
        string='Read',
        required=False,
        readonly=True,
        help="Group can read existing model records"
    )

    perm_write = fields.Boolean(
        string='Update',
        required=False,
        readonly=True,
        help="Group can update existing model records"
    )

    perm_unlink = fields.Boolean(
        string='Delete',
        required=False,
        readonly=True,
        help="Group can delete existing model records"
    )

    crud = fields.Integer(
        string='Crud',
        required=False,
        readonly=True,
        help='Create, read, update, delete bits (decimal)'
    )

    # --------------------------OVERWRITTEN METHODS----------------------------

    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """

        tools.drop_view_if_exists(cr, self._table)

        cr.execute("""
            create or replace view {} AS (
                {}
            )
        """.format(self._table, self._sql_query))

    # ---------------------------LONG TEXT STRINGS-----------------------------

    _sql_query = """
        WITH access_data AS (
            WITH model_data AS (
                WITH unique_model_data AS (
                    SELECT DISTINCT
                        ON (res_id) "module",
                        "name",
                        "res_id"
                    FROM
                        ir_model_data
                    WHERE
                        model = 'ir.model'
                    ORDER BY
                        res_id ASC,
                        "id" ASC
                ) SELECT
                    ir_module_module."id" AS module_id,
                    ir_module_module."name" AS module_name,
                    ir_model."id" AS model_id,
                    ir_model."model" AS model_name,
                    unique_model_data."name" AS model_xml_id,
                    CONCAT (
                        ir_module_module."name",
                        '.',
                        unique_model_data."name"
                    ) AS model_fully_qualified_xml_id
                FROM
                    ir_model
                INNER JOIN unique_model_data
                    ON unique_model_data.res_id = ir_model."id"
                INNER JOIN ir_module_module
                    ON ir_module_module."name" = unique_model_data."module"
                ORDER BY
                    model_fully_qualified_xml_id
            ) SELECT
                COALESCE(ir_model_access.perm_create, 'f') AS perm_create,
                COALESCE(ir_model_access.perm_read, 'f') AS perm_read,
                COALESCE(ir_model_access.perm_write, 'f') AS perm_write,
                COALESCE(ir_model_access.perm_unlink, 'f') AS perm_unlink,
                CASE WHEN perm_create = 't' THEN 8 ELSE 0 END +
                CASE WHEN perm_read = 't' THEN 4 ELSE 0 END +
                CASE WHEN perm_write = 't' THEN 2 ELSE 0 END +
                CASE WHEN perm_unlink = 't' THEN 1 ELSE 0 END
                AS crud,
                model_data.*,
                groups_implied.*
            FROM
                model_data
            LEFT JOIN ir_model_access
                ON model_data.model_id = ir_model_access.model_id
            LEFT JOIN report_groups_implied AS groups_implied
                ON ir_model_access.group_id = groups_implied.implied_id
        ) SELECT
            ROW_NUMBER() OVER() AS "id",
            min(module_id) AS model_module_id,
            min(module_name) AS model_module_xml_id,
            model_id,
            min(model_name) AS model_name,
            min(model_xml_id) AS model_xml_id,
            min(model_fully_qualified_xml_id)
                AS model_fully_qualified_xml_id,
            bool_or(perm_create) AS perm_create,
            bool_or(perm_read) AS perm_read,
            bool_or(perm_write) AS perm_write,
            bool_or(perm_unlink) AS perm_unlink,
            bit_or(crud) AS crud,
            min(group_category_id) AS group_category_id,
            min(group_category_fully_qualified_xml_id)
                AS group_category_fully_qualified_xml_id,
            min(group_module_id) AS group_module_id,
            min(group_module_xml_id) AS group_module_xml_id,
            group_id,
            min(group_name) AS group_name,
            min(group_xml_id) AS group_xml_id,
            min(group_fully_qualified_xml_id)
                AS group_fully_qualified_xml_id,
            min(implied_category_id) AS implied_category_id,
            min(implied_category_fully_qualified_xml_id)
                AS implied_category_fully_qualified_xml_id,
            min(implied_module_id) AS implied_module_id,
            min(implied_module_xml_id) AS implied_module_xml_id,
            min(implied_id),
            min(implied_name) AS implied_name,
            min(implied_xml_id) AS implied_xml_id,
            min(implied_fully_qualified_xml_id)
                AS implied_fully_qualified_xml_id
        FROM
            access_data
        GROUP BY model_id, group_id
    """
