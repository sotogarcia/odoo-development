# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, api
from openerp.tools.translate import _
from logging import getLogger


_logger = getLogger(__name__)


class IrUiView(models.Model):
    """ Overwrites ir.ui.view adding adding the possibility of reload views
        from XML files
    """

    _inherit = 'ir.ui.view'

    # --------------------------- RELOAD BEHAVIOR -----------------------------

    @api.model
    def reload(self, ids):
        """ Public method used in button added to the `base.view_view_tree`

            :param ids [integer]: list of ir.ui.view identifiers
        """
        print('reload')
        for view_id in ids:
            view_obj = self.env['ir.ui.view']
            view_set = view_obj.browse(view_id)

            if view_set:
                print('view_set', view_set)

                dict_xml_id = view_set.get_xml_id()
                xml_id = dict_xml_id and dict_xml_id[view_id]

                if xml_id:
                    model_obj = self.env['ir.model']
                    model_obj.reload('ir.ui.view', view_id, xml_id)
                else:
                    self._log(3, 'NOXID', view_set)
            else:
                self._log(3, 'NOID', view_id)

        return {
            'type': 'ir.actions.client',
            'tag': 'reload',
        }
    # ---------------------------- LOG MESSAGES -------------------------------

    def _log(self, level, message, *args, **kwargs):
        """ Outputs an formated string in log

            :param level (int): 1=> debug, 2=> info, 3=> warning, 4=> error
            :param message (basestring): name of the message
        """

        methods = ['debug', 'info', 'warning', 'error']
        log = getattr(_logger, methods[level])

        message_format = self._messages[message]
        msg = message_format.format(*args, **kwargs)
        log(msg)

    _messages = {
        u'NOXID': _(u'Failed refeshing the view, there is not an xml id '
                    u'for \'{}\''),
        u'NOID': _(u'Failed refeshing the view, invalid view id: {}'),
    }
