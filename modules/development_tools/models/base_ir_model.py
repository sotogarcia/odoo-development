# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, api
from openerp.tools.translate import _
from logging import getLogger

from openerp.tools import convert_file
from openerp.modules.module import load_information_from_description_file, \
    get_module_resource

from xml.etree import ElementTree


_logger = getLogger(__name__)


class IrModel(models.Model):
    """ Overwrites ir.ui.view adding adding the possibility of reload views
        from XML files
    """

    _inherit = 'ir.model'

    @api.model
    def reload(self, model, _id, xml_id):
        result = False

        m_data_domain = [('model', '=', model), ('res_id', '=', _id)]
        m_data_obj = self.env['ir.model.data']
        m_data_set = m_data_obj.search(m_data_domain)

        if m_data_set:
            self._reload(m_data_set.module, model, m_data_set.name, _id)
        else:
            self._log(3, 'NOXID', _id)

        return result

    def _reload(self, mod_name, model_name, ex_name, res_id):
        """ Private reload method which contains the real behavior to load
            each one of the views.
        """

        self._log(1, 'UPD', mod_name, ex_name)

        try:
            # STEP 1: Find XML file with given external ID
            xml_files = self._get_xml_files(mod_name, demo=False)
            xml_file = self._search_in_files(mod_name, xml_files, ex_name)

            # STEP 2: Call the update method
            convert_file(
                self.env.cr,
                mod_name,
                xml_file,
                {model_name: res_id},
                mode='update',
                noupdate=False,
                kind='data'
            )
        except Exception as ex:
            self._log(3, 'UPDFAIL', mod_name, ex_name, ex)

    # ------------------------- AUXILIARY FUNCTIONS ---------------------------

    def _search_in_files(self, mod_name, files, identifier):
        """ Returns the path of the first file in list which contains the
            given external identifier (name)

            :param mod_name (bool): module name to get root path
            :param files ([basestring]): XML file paths list
            :param identifier (basestring): external identifier without module

            :return: path of the file or None
        """

        mod_name = mod_name
        xpath = './/record[@id=\'{}\']'.format(identifier)

        for f in files:
            path = get_module_resource(mod_name, f)
            tree = ElementTree.parse(path)
            root = tree.getroot()

            if root.findall(xpath):
                return f

        return None

    def _get_xml_files(self, mod_name, demo=False):
        """ Gets all XML file paths from module manifest file

            :param mod_name (basestring): name of the module
            :param demo (bool): include demo XML files

            :return ([basestring]): XML relative file paths
        """
        data = []

        info = load_information_from_description_file(mod_name)
        if info:
            data = info['data'] if 'data' in info else []

            if demo:
                data += info['demo'] if 'demo' in info else []

        return filter(lambda x: x.endswith('.xml'), data)

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
        u'UPD': _(u'Refreshing resource: {}.{}'),
        u'NOXID': _(u'Failed refeshing the resource, there is not an xml id '
                    u'for \'{}\''),
        u'UPDFAIL': _(u'Resource {}.{} could not be upgraded, system has '
                      u'said {}')
    }
