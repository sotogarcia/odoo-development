# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class IrActionsActWindow(models.Model):
    """ Adds a method to safely execute the action
    """

    _name = 'ir.actions.act_window'
    _inherit = ['ir.actions.act_window']

    @api.model
    def safe_execute(self):
        """ Evaluates the context searching model name and record ids, browse
            records and run each one.
        """

        ctx = self.env.context

        if self._context_has_items(ctx):
            model, ids = self._get_from_context(ctx)
            if model and model == self._name and ids:
                jobs = self._get_jobs(model, ids)
                for action in jobs:
                    return self._safe_execute(action)

    def _safe_execute(self, action):
        """ Executes a act_window action inside a try except block and log results

            :param action (ir.actions.act_window): action to be executed
        """

        try:
            _logger.info(self._executing_msg.format(action, action.name))
            values = action.with_context({}).read()
            return values[0] if values else False
        except Exception as ex:
            msg = self._error_msg.format(action, action.name, ex)
            _logger.error(msg)
            return False

    def _context_has_items(self, ctx):
        """ Verifies that the context has the attributes: active_model and
            active_ids

            :param ctx (dict): context that will be processed
            :return (bool): True if both attributes exist or False otherwise
        """

        return 'active_model' in ctx and 'active_ids' in ctx

    def _get_from_context(self, ctx):
        """ Gets the active_model and active_ids attributes from context

            :param ctx (dict): context that will be processed
            :return: active_model, active_ids
        """

        return ctx['active_model'], ctx['active_ids']

    def _get_jobs(self, model, ids):
        """ Gets all jobs with id in ids

            :param (str): name of the model
            :ids ([int]): list of ids of the records to be retrieved
            :return (recordset): recordset with the items have been retrieved
        """
        return self.env[model].browse(ids)

    # ------------------------- LONG TEXT VARIABLES ---------------------------

    _executing_msg = _(u'Executing the act_window action: {} / {}')

    _error_msg = _(u'''
        An error has occurred when Odoo was trying to run a act_window action.
        Action: {} / {}
        Exception: {}
    ''')
