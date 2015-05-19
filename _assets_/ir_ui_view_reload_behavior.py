

    def _reload(self):
        """ Private reload method which contains the real behavior to load
            each one of the views.
        """

        self.ensure_one()

        try:
            module = self._get_module()

            # STEP 1: Get all needed data
            mod_name = module.name
            x_name = self._get_external_name(mod_name)
            xml_files = self._get_xml_files(mod_name, demo=False)
            xml_file = self._search_in_files(mod_name, xml_files, x_name)

            assert mod_name and x_name and xml_file, \
                self._messages['RI'] % (mod_name, x_name, self.id, xml_file)

            self._log(1, 'RI', mod_name, x_name, self.id, xml_file)

            # STEP 2: Call the update method
            convert_file(
                self.env.cr,
                mod_name,
                xml_file,
                {x_name: self.id},
                mode='update',
                noupdate=False,
                kind='data'
            )

        except Exception as ex:
            self._log(3, 'RF', self.xml_id, ex)

    # ------------------------- AUXILIARY FUNCTIONS ---------------------------

    def _get_module(self):
        """ Returns the module in which view has been defined
        """

        _id = self.id

        # STEP 1: Locate module name in ir.model.data using model and id
        m_data_domain = [('model', '=', 'ir.ui.view'), ('res_id', '=', _id)]
        m_data_obj = self.env['ir.model.data']
        m_data_set = m_data_obj.search(m_data_domain)
        m_data_set.ensure_one()  # Should be unique

        # STEP 2: Locate module by name in ir.module.module
        module_domain = [('name', '=', m_data_set.module)]
        module_obj = self.env['ir.module.module']
        module_set = module_obj.search(module_domain)
        module_set.ensure_one()  # Should be unique

        return module_set

    def _get_external_name(self, mod_name):
        """ Returns the external name ir.model.data->name from fully qualified
            external ID

            :param mod_name (basestring): name of the module
            :return (basestring): external name
        """

        start = len(mod_name) + 1
        return self.xml_id[start:]

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
        u'RS': _(u'Try to update the following views: {}'),
        u'RI': _(u'Update info: {{module: {}, name: {}, id: {}, file: {}}}'),
        u'RF': _(u'Updating {} has fail. System has said: {}.'),
    }
