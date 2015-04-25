# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from logging import getLogger
from openerp.tools.translate import _

_logger = getLogger(__name__)


class DevDomainTester(models.TransientModel):
    """ Usefull wizard to test diferent domains and contexts

    Fields:
        model_id (Many2one): ir.model upon which domain will be applied
        view_id (Many2one): ir.ui.view will be used to watch the results
        domain_string (Char): domain will be tested
        context_string (Char): context used in test
    """

    _name = 'dev.domain.tester'
    _description = _(u'Usefull wizard to test diferent domains and contexts')

    _rec_name = 'name'
    _order = 'name ASC'

    # -----------------------------ENTITY FIELDS-------------------------------

    name = fields.Char(
        string='Name',
        required=True,
        readonly=True,
        default=_('Domain tester'),
        help="Wizard name",
        size=25,
        translate=True
    )

    model_id = fields.Many2one(
        string='Model',
        required=True,
        readonly=False,
        default=lambda self: self._default_model_id(),
        help='Choose an Odoo existing model',
        comodel_name='ir.model',
        ondelete='restrict',
    )

    view_id = fields.Many2one(
        string='View',
        required=True,
        readonly=False,
        default=None,
        help='Choose a valid view for model',
        comodel_name='ir.ui.view',
        ondelete='restrict'
    )

    domain_string = fields.Char(
        string='Domain',
        required=False,
        readonly=False,
        default='[]',
        help='Write the domain which will be tested',
        size=255,
        translate=False
    )

    context_string = fields.Char(
        string='Context',
        required=False,
        readonly=False,
        default='{}',
        help='Write the context which will be tested',
        size=255,
        translate=False
    )

    # ------------------------AUXILIARY FIELD METHODS--------------------------

    def _default_model_id(self):
        """ Gets the ir.model record which contains the res.partner model
            information.

            :return: ir.model('base.model_res_partner')
        """
        return self.env.ref('base.model_res_partner')

    @api.onchange('model_id')
    def _onchange_model_id(self):
        """ Updates view_id domain and value when model_id has been changed.

            - domain: limits the views shown to which belong to the previously
            selected model.
            - value: this method sets view_id value to the valid tree view
            with the lower id if exists or, otherwise it cleans the previously
            entered value.

            :returns: dictionary with the new field domain
        """

        model_model = self.model_id.model if self.model_id else False

        domain = ['&', ('model', '=', model_model), ('type', '=', 'tree')]
        view_obj = self.env['ir.ui.view']
        self.view_id = view_obj.search(domain, limit=1, order='id ASC')

        return {
            'domain': {'view_id': [('model', '=', model_model)]}
        }

    # ----------------------------PUBLIC METHODS-------------------------------

    @api.multi
    def cmd_execute(self, values):
        """ Shows the choosen ir.ui.view for selected ir.model and closes this
            wizard.

            :return: appropriate act_window if user has choosen model and view
            or False otherwise
        """
        self.ensure_one()

        result = False

        if self.model_id and self.view_id:
            self._log_entered_values()
            result = self._build_act_window()

        return result

    # ---------------------------AUXILIARY METHODS-----------------------------

    def _log_entered_values(self):
        """ Outputs the values entered to the log file """

        _logger.info("""
                Model: {}
                Views: {}
                Domain: {}
                Context: {}
            """.format(
                self.model_id,
                self.view_id,
                self.domain_string,
                self.context_string
            )
        )

    def _build_act_window(self):
        """ Builds a new act_window with the values entered in wizard

            :return: a built act_window if model_id and view_id have been
            filled or False otherwise
        """

        return {
            'model': 'ir.actions.act_window',
            'type': 'ir.actions.act_window',
            'name': self.model_id.model,
            'res_model': self.model_id.model,
            'view_mode': self.view_id.type,
            'view_type': 'form',
            'view_id': self.view_id.id,
            'target': 'form',
            'domain': self.domain_string or '[]',
            'context': self.context_string or '{}'
        } if self.model_id and self.view_id else False
