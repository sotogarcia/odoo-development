# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class DevelopmentToolsConfigSettings(models.TransientModel):
    """ Module config settings

    Fields:
      email_to (Char): Address will be used to send captured email messages.

    """

    _name = 'development_tools.config.settings'
    _inherit = ['res.config.settings']

    _description = u'Module config settings'

    _rec_name = 'id'
    _order = 'id ASC'

    _external_id = 'development_tools.development_tools_config_settings_data'

    # ---------------------------- ENTITY FIELDS ------------------------------

    email_to = fields.Char(
        string='Email to',
        required=False,
        readonly=False,
        index=False,
        help='Address will be used to send captured email messages',
        size=50,
        translate=False
    )

    email_capture = fields.Boolean(
        string='Capture emails',
        required=False,
        readonly=False,
        index=False,
        default=False,
        help='Check it to capture outgoing email messages'
    )

    # --------------------------- PUBLIC METHODS ------------------------------

    @api.model
    def get_default_email_values(self, fields):

        return {
            'email_to': False,
            'email_capture': False,
        }

    @api.one
    def set_email_values(self):

        record = self.env.ref(self._external_id)

        values = {
            'email_to': self.email_to,
            'email_capture': self.email_capture,
        }

        record.write(values)
