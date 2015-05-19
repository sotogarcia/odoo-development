# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp.http import route, request, Controller, redirect_with_hash
import openerp.addons.web.controllers.main as webmain
from openerp.tools.translate import _
from logging import getLogger
import werkzeug

_logger = getLogger(__name__)


class Home(webmain.Home):
    """ Overrides web.Home controller and adds auto-debug mode behavior

        Routes:
          /web: Odoo home url
    """

    @route()
    def web_client(self, s_action=None, **kw):
        result = None

        if not request.debug and request.db and self._get_debug_mode():
            _logger.info(self._debug_message)
            result = self._build_debug_response()

        return result or super(Home, self).web_client(s_action, **kw)

    def _get_debug_mode(self):
        config = request.env['development_tools.config.settings']
        debug = config.get_debug_mode()

        return debug == True

    def _build_debug_response(self):
        result = None

        try:
            query = request.params
            query.update({'debug': u''})
            url = '/web?' + werkzeug.url_encode(query)
            result = redirect_with_hash(url)
        except Exception as ex:
            _logger.error(self._error_response.format(ex))

        return result

    # ------------------------ LONG CHARACTER STRING --------------------------

    _debug_message = _(u'Auto-redirect to enter in debug mode')

    _error_response = _(
        u'The debug response could not be built.\n'
        u'System has said: {}'
    )




