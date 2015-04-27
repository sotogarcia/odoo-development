# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger
from cStringIO import StringIO
import sys

_logger = getLogger(__name__)


class DevDomainTester(models.TransientModel):
    """ Wizard which can be used to test python code inside Odoo

    Fields:
      model_id: Model will be used in the server action
      is_action: Code will be executed as server action
      code: Python code to be executed
      stdout: Captured system stdout text
      exception: Last captured exception
      info: Information about available variables
    """

    _name = 'dev.code.tester'
    _description = u'Wizard to test Python code inside Odoo'

    _rec_name = 'id'
    _order = 'id ASC'

    # ---------------------------- ENTITY FIELDS ------------------------------

    model_id = fields.Many2one(
        string='Model',
        required=True,
        readonly=False,
        help='Model will be used in server action',
        comodel_name='ir.model',
        ondelete='restrict',
        default=lambda self: self._default_model_id()
    )

    is_action = fields.Boolean(
        string='Server action',
        required=False,
        readonly=False,
        default=False,
        help="Execute entered code in a ir.action.server"
    )

    code = fields.Text(
        string='Code',
        required=True,
        readonly=False,
        default='print (\'Hola mundo!\')',
        help='Code will be executed',
        translate=False
    )

    # -------------------------- MANAGEMENT FIELDS ----------------------------

    stdout = fields.Text(
        string='Output',
        required=False,
        readonly=True,
        default='',
        help='Catch the stdout',
        translate=False
    )

    exception = fields.Char(
        string='Exception',
        required=False,
        readonly=True,
        default=None,
        help='Catch the exception',
        size=255,
        translate=False
    )

    info = fields.Html(
        string='Information',
        required=False,
        readonly=True,
        default=lambda self: self._default_info(),
        compute=lambda self: self._compute_info(),
        help='Information about available variables'
    )

    # ----------------------- AUXILIARY FIELD METHODS -------------------------

    @api.onchange('model_id')
    def _onchange_model_id(self):
        for record in self:
            record.info = self._default_info()

    @api.multi
    @api.depends('model_id')
    def _compute_info(self):
        for record in self:
            record.info = self._default_info()

    @api.returns('ir.model')
    def _default_model_id(self):
        return self.env.ref('base.model_res_partner')

    def _default_context(self):
        return self.env.context or '{}'

    def _default_info(self):
        return self.info_format.format(
            self.model_id.model if self.model_id else '',
            'logging.getLogger(__name__)',
            self.env.context,
            'self.stdout = \'\''
        )

    # --------------------------- PUBLIC METHODS ------------------------------

    @api.multi
    def cmd_execute(self):
        """ Builds a new server action to execute the inserted in code field.

            :return: appropriate ir.actions.server if user has choosen model
            and inserted some code or False otherwise
        """
        self.ensure_one()

        result = False

        if self.model_id and self.code:
            self._log_entered_values()
            # result = self._build_ir_action_server()

        if self.is_action:
            self._call_action()
        else:
            self._safe_exec()

        return result

    # -------------------------- AUXILIARY METHODS ----------------------------

    def _call_action(self):
        action_xid = 'developement_tools.action_development_code_tester_server'
        action = self.env.ref(action_xid)
        ctx = self.env.context().copy()
        ctx.update({'active_model': self.model_id})
        action.with_context(ctx).run()

    def _begin_execute(self):
        """ Switch encoding to UTF-8 and capture stdout to an StringIO object

            :return: current captured sys.stdout
        """

        new_stdout = StringIO()

        self._encoding = sys.getdefaultencoding()
        reload(sys)
        sys.setdefaultencoding('utf-8')

        self._stdout = sys.stdout
        sys.stdout = new_stdout

        return new_stdout

    def _restore_encoding(self):
        """ Restores previous encoding and release stdout
        """

        if hasattr(self, '_stdout') and self._stdout:
            sys.stdout = self._stdout

        if hasattr(self, '_encoding') and self._encoding:
            reload(sys)
            sys.setdefaultencoding(self._encoding)

    def _clear(self):
        """ Clears the stdout field content """

        self.stdout = ''

    def _safe_exec(self):
        """ Executes the code entered """

        self.exception = None
        stdout = self._begin_execute()

        try:
            # Available variables
            ctx = self.env.context.copy()
            obj = self.env[self.model_id.model] if self.model_id else None
            log = _logger
            clear = self._clear

            exec(self.code.encode('utf-8'))

            self.stdout += stdout.getvalue()

        except Exception as ex:
            self.exception = ex

        self.info = self._default_info()
        sys.stdout = stdout
        self._restore_encoding()

    def _log_entered_values(self):
        """ Outputs the values entered to the log file """

        _logger.info(u"""
                Model: {}
                Code: {}
                Context: {}
            """.format(
                self.model_id,
                self.code,
                self.env.context
            )
        )

    # ------------------------ LONG TEXT ATTRIBUTES ---------------------------

    info_format = u"""
        <table class="oe_form_group">
            <tbody>
                <tr class="oe_form_group_row">
                    <td class="oe_form_group_cell oe_form_group_cell_label">
                        <b>obj</b>
                    </td>
                    <td class="oe_form_group_cell">{}</td>
                </tr>
                <tr>
                    <td class="oe_form_group_cell oe_form_group_cell_label">
                        <b>log</b>
                    </td>
                    <td class="oe_form_group_cell">{}</td>
                </tr>
                <tr>
                    <td class="oe_form_group_cell oe_form_group_cell_label">
                        <b>ctx</b>
                    </td>
                    <td class="oe_form_group_cell">{}</td>
                </tr>
                <tr>
                    <td class="oe_form_group_cell oe_form_group_cell_label">
                        <b>clear()</b>
                    </td>
                    <td class="oe_form_group_cell">{}</td>
                </tr>
            </tbody>
        </table>
    """
