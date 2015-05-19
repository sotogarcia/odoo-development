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


class ReportFieldDetail(models.Model):
    """ Detailed information about fields

    Fields:
      field_id (Char): Parent model in delegated inheritance.

    """

    _name = 'report.field.detail'
    _description = u'Report field detail'

    _inherits = {'ir.model.fields': 'field_id'}
    _auto = False
    _table = 'report_field_detail'

    _rec_name = 'name'
    _order = 'name ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    field_id = fields.Many2one(
        string='Field',
        required=True,
        readonly=True,
        index=False,
        default=None,
        help=False,
        comodel_name='ir.model.fields',
        domain=[],
        context={},
        ondelete='restrict',
        auto_join=False
    )

    lang = fields.Char(
        string='Language',
        required=True,
        readonly=False,
        index=False,
        default='es_ES',
        help='Language used to show in reports',
        size=50,
        translate=False,
        compute=lambda self: self._compute_lang()
    )

    size = fields.Integer(
        string='Size',
        required=False,
        readonly=True,
        index=False,
        default=1000,
        help='Size of the text (char fields only)',
        compute=lambda self: self._compute_size()
    )

    digits = fields.Char(
        string='Digits',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='A pair (total, decimal), or a function',
        size=50,
        translate=False,
        compute=lambda self: self._compute_digits()
    )

    initial = fields.Char(
        string='Default',
        required=False,
        readonly=True,
        index=False,
        default=None,
        help='Field default value',
        size=50,
        translate=False,
        compute=lambda self: self._compute_initial()
    )

    store = fields.Boolean(
        string='Store',
        required=False,
        readonly=True,
        index=False,
        default=False,
        help='Field will stored',
        compute=lambda self: self._compute_store()
    )

    company_dependent = fields.Boolean(
        string='Company dependent',
        required=False,
        readonly=True,
        index=False,
        default=False,
        help='Is company dependent',
        compute=lambda self: self._compute_company_dependent()
    )

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.multi
    @api.depends('field_id')
    def _compute_lang(self):
        """ Gets the language used by the current user and sets it as `lang`
            field value
        """

        user_id = self.env['res.users'].browse(self.env.uid)

        for record in self:
            record.lang = user_id.lang

    @api.multi
    @api.depends('field_id')
    def _compute_digits(self):
        for record in self:
                record.digits = record._get_attribute('digits')

    @api.multi
    @api.depends('field_id')
    def _compute_size(self):
        for record in self:
                record.size = record._get_attribute('size')

    @api.multi
    @api.depends('field_id')
    def _compute_initial(self):
        for record in self:
            record.initial = record._get_default_value()

    @api.multi
    @api.depends('field_id')
    def _compute_store(self):
        for record in self:
            record.store = record._get_attribute('store')

    @api.multi
    @api.depends('field_id')
    def _compute_company_dependent(self):
        for record in self:
            record.company_dependent = record._get_attribute(
                'company_dependent')

    # -------------------------- AUXILIARY METHODS ----------------------------

    def _get_attribute(self, attr):
        """ Retrieves the value for an attribute of the field

            :param self (ir.model.field): singleton
            :param attr (char): name of the attribute will be retrieved.
        """

        self.ensure_one()

        model_obj = self.env[self.model_id.model]
        model_set = model_obj.browse(self.model_id.id)
        attrs_dict = model_set.fields_get(self.name)

        field, attrs = attrs_dict.popitem()

        return attrs[attr] if attrs and attr in attrs else None

    def _get_default_value(self):
        """ Retrieves the field default value from model

            TODO: method gets value from private model attribute, it should be
            retrieved in other way
            :return (str): returns the default value as string
        """
        self.ensure_one()

        result = None

        model_obj = self.env[self.model_id.model]
        if model_obj._defaults and self.name in model_obj._defaults:
            try:
                result = unicode(model_obj._defaults[self.name])
            except Exception as ex:
                _logger.warning(ex)

        return result

    # -------------------------- OVERWITEN METHODS ----------------------------

    def init(self, cr):
        """ Build database view which will be used as module origin

            :param cr: database cursor
        """
        self._sql_query = """
            SELECT
                "id" AS "id",
                "id" as field_id
            FROM ir_model_fields
            WHERE model <> '{}'
            ORDER BY {}
        """.format(self._name, self._order)

        drop_view_if_exists(cr, self._table)
        cr.execute(
            'create or replace view {} as ({})'.format(
                self._table,
                self._sql_query
            )
        )
