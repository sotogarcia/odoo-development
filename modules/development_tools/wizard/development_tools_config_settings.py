# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.tools.safe_eval import safe_eval
from logging import getLogger


_logger = getLogger(__name__)


class DevelopmentToolsConfigSettings(models.TransientModel):
    """ Module config settings

    Fields:
      email_to (Char): Address will be used to send captured email messages
      email_capture (Boolean): Check it to capture outgoing email messages
      developing_modules_enabled (Boolean): Sets the filter as default filter
      in Local modules views
      developing_module_ids (Many2many): Select items you want to display by
      default Local modules views
      search_default_app (Boolean): Enable search_default_app filter in the
      Local modules view
    """

    _name = 'development_tools.config.settings'
    _description = u'Development tools config settings'

    _inherit = ['res.config.settings']

    _rec_name = 'id'
    _order = 'id ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    email_to = fields.Char(
        string='Email to',
        required=False,
        readonly=False,
        index=False,
        help='Address will be used to send captured email messages',
        size=50,
        translate=False,
        default='development_tools@yopmail.com',
    )

    email_capture = fields.Boolean(
        string='Capture emails',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check it to capture outgoing email messages',
    )

    developing_modules_enabled = fields.Boolean(
        string='Set as default filter',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Sets the filter as default filter in Local modules views'
    )

    developing_module_ids = fields.Many2many(
        string='Modules shown',
        required=False,
        readonly=False,
        index=False,
        default=None,
        help='Select items you want to display by default Local modules views',
        comodel_name='ir.module.module',
        domain=[],
        context={},
        limit=None,
        manual=True,
        compute=lambda self: self._compute_developing_module_ids(),
        inverse=lambda self: self._inverse_developing_module_ids()
    )

    search_default_app = fields.Boolean(
        string='Search default app filter',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Enable search_default_app filter in the Local modules view'
    )

    # ----------------------- COMPUTED FIELD METHODS --------------------------

    def _compute_developing_module_ids(self):
        for record in self:
            record.developing_module_ids = record.get_developing_module_ids()

    def _inverse_developing_module_ids(self):
        try:
            ids = [module.id for module in self.developing_module_ids]
            name = 'filter_model_name_whithout_module_development_modules'
            filter_set = self.env.ref('{}.{}'.format(self._module, name))
            filter_set.domain = unicode([('id', 'in', ids or [-1])])
        except Exception as ex:
            _logger.error('_inverse_developing_module_ids: %s' % ex)

    # --------------------- RES.CONFIG.SETTINGS METHODS -----------------------

    @api.model
    def get_default_values(self, values):
        return dict(
            email_to=self.get_email_to(),
            email_capture=self.get_email_capture(),
            developing_modules_enabled=self.get_developing_modules_enabled(),
            developing_module_ids=self.get_developing_module_ids(),
            search_default_app=self.get_search_default_app(),
        )

    @api.one
    def set_default_values(self):
        self._set_email_to()
        self._set_email_capture()
        self._set_developing_modules_enabled()
        self._set_developing_module_ids()
        self._set_search_default_app()

    # ------------------------- GETTERS AND SETTERS ---------------------------

    def get_email_to(self):
        param = self._get_parameter('email_to')
        return param.value if param else None

    def _set_email_to(self):
        param = self._get_parameter('email_to', force=True)
        param.value = self.email_to

    def get_email_capture(self):
        param = self._get_parameter('email_capture')
        return self._safe_eval(param.value, bool) if param else None

    def _set_email_capture(self):
        param = self._get_parameter('email_capture', force=True)
        param.value = unicode(self.email_capture)

    def get_developing_modules_enabled(self):
        value = None

        try:
            name = 'filter_model_name_whithout_module_development_modules'
            filter_set = self.env.ref('{}.{}'.format(self._module, name))
            value = filter_set.is_default
        except Exception as ex:
            msg = self._not_retrieved.format('developing_modules_enabled', ex)
            _logger.error(msg)

        return value

    def _set_developing_modules_enabled(self):
        try:
            name = 'filter_model_name_whithout_module_development_modules'
            filter_set = self.env.ref('{}.{}'.format(self._module, name))
            filter_set.is_default = self.developing_modules_enabled
        except Exception as ex:
            msg = self._not_set('developing_modules_enabled', ex)
            _logger.error(msg)

    def get_developing_module_ids(self):
        value = None

        try:
            name = 'filter_model_name_whithout_module_development_modules'
            filter_set = self.env.ref('{}.{}'.format(self._module, name))
            domain = self._safe_eval(filter_set.domain, list)
            value = filter(lambda x: x > 0, domain[0][2])
        except Exception as ex:
            msg = self._not_retrieved.format('developing_module_ids', ex)
            _logger.error(msg)

        return value

    def _set_developing_module_ids(self):
        try:
            ids = [module.id for module in self.developing_module_ids]
            name = 'filter_model_name_whithout_module_development_modules'
            filter_set = self.env.ref('{}.{}'.format(self._module, name))
            filter_set.domain = unicode([('id', 'in', ids or [-1])])
        except Exception as ex:
            msg = self._not_set('developing_module_ids', ex)
            _logger.error(msg)

    def get_search_default_app(self):
        value = False

        try:
            action_set = self.env.ref('base.open_module_tree')
            context = self._safe_eval(action_set.context, dict)
            if 'search_default_app' in context:
                value = context['search_default_app'] in [1, True]
            else:
                value = False
        except Exception as ex:
            msg = self._not_retrieved.format('search_default_app', ex)
            _logger.error(msg)

        return value

    def _set_search_default_app(self):
        try:
            action_set = self.env.ref('base.open_module_tree')
            context = self._safe_eval(action_set.context, dict)
            value = 1 if self.search_default_app else 0
            context.update({'search_default_app': value})
            action_set.context = unicode(context)
        except Exception as ex:
            msg = self._not_set.format('search_default_app', ex)
            _logger.error(msg)

    # --------------------------- #PUBLIC METHODS -----------------------------

    def get_value(self, field_name):
        """ Calls the appropiate method to retrieve the value of the field
            with the given name and returns its value

            :param field_name (char): name of the field

            :returns: returns retrieved value or None
        """

        result = None

        try:
            method_name = 'get_{}'.format(field_name)
            method = getattr(self, method_name)
            result = method()
        except Exception as ex:
            msg = self._not_value.format(field_name, ex)
            _logger.error(msg)

        return result

    # -------------------------- AUXILIARY METHODS ----------------------------

    def _get_parameter(self, field_name, force=False, default=u''):
        """ Gets the ir.config_parameter for the field

            :param field_name (char): name of the field
            :force (bool): create record if not exists
            :default (basestring): default parameter value if it is creted new

            :return (ir.config_parameter): recordset with a record or empty

            :note: Parameters could be searched by their external ids but if
            they are created anew, then they could not be found

            :note: Limit the search is not needed because the `key`column has
            unique index constraint

            :note: If there is not any matching record, the returned set will
            be empty
        """

        param_name = u'{}.{}'.format(self._module, field_name)

        param_domain = [('key', '=', param_name)]
        param_obj = self.env['ir.config_parameter']
        param_set = param_obj.search(param_domain)

        if not param_set and force:
            param_set = param_obj.create(
                {'key': param_name, 'value': default}
            )

        return param_set

    def _safe_eval(self, value_str, types=None):
        """ Try to convert an string in a value of one of the given types

            :param value_str (basestring): string to be converted
            :param types (type): type or iterable set of them

            :return: value of one of the types if it could be converted or None
        """

        value = None

        try:
            types = self._iterable(types)
            value = safe_eval(value_str)

            if not type(value) in types:
                msg = self._check_type_msg.format(value_str, types)
                _logger.error(msg)
                value = None

        except Exception as ex:
            _logger.error(self._safe_eval_msg.format(value_str, ex))

        return value

    def _iterable(self, item):
        """ Ensures the given item is iterable

            :param: item to be tested

            :return: item if it's iterable or the item within a list
        """
        try:
            iter(item)
            item.__iter__()
        except:
            return [item]
        else:
            return item or [None]

    # ----------------------- LONG CHARACTER STRINGS --------------------------

    _safe_eval_msg = _(
        u'Value \'{}\' could not be evaluated\n'
        u'System has said: {}'
    )

    _check_type_msg = _(
        u'Wrong type value `{}`, one of the following was expected: `{}`'
    )

    _not_retrieved = _(
        u'The value `{}` could not be retrieved\n'
        u'System has said: {}'
    )

    _not_set = _(
        u'The value `{}` could not be set\n'
        u'System has said: {}'
    )

    _not_value = _(
        u'Could not retrive value for field `{}`\n'
        u'System has said: {}'
    )
