# -*- coding: utf-8 -*-
###############################################################################
#    License, author and contributors information in:                         #
#    __openerp__.py file at the root folder of this module.                   #
###############################################################################

from openerp import models, fields, api
from openerp.tools.translate import _
from openerp.modules.module import get_module_filetree, get_module_resource, get_module_path, init_module_models
from logging import getLogger
from shutil import copy2
from os import remove, path, walk, sep as dir_sep
import compileall


_logger = getLogger(__name__)


class IrModuleModule(models.Model):
    """ Extends the module funcionality with needed methods to allow dynamical
        upgrades in development stage


    """

    _inherit = 'ir.module.module'

    @api.multi
    def button_immediate_upgrade(self):
        """ Originaly method upgrades the selected module(s) immediately and
            fully, return the next res.config action to execute

            This method overloading adds the necessary functionality to
            dynamically recompile the module
        """

        self._compile()

        return super(IrModuleModule, self).button_immediate_upgrade()

    # -------------------------- COMPILE BEHAVIOR -----------------------------

    def _compile(self):

        def filter_pyc(parents, name, contents):
            return name.endswith(u'.pyc')

        try:

            # STEP 1: Backup of all `pyc` files within the module information
            self.log(1, 'backing_up', self.name)

            files = self._get_resource_paths(filter_pyc)
            for pyc_file in files:
                self._backup(pyc_file)

            self.log(1, 'backing_done', self.name)

            # STEP 2: Compile the module
            try:
                self.log(1, 'compiling', self.name)

                module_path = get_module_path(self.name)
                compileall.compile_dir(module_path, True)

                for pyc_file in files:
                    _logger.warning('Reload %s' % pyc_file)
                    reload(pyc_file)

                self.log(1, 'compilation_done', self.name)
            except Exception as ex:
                # STEP 3: Restore old files if compilation fails
                self.log(1, 'compilation_fail', self.name)

                for pyc_file in files:
                    self._backup(pyc_file, restore=True)

                self.log(1, 'restoring_done', self.name)

                raise ex

            # STEP 4: Update modules
            m_data_domain = [
                ('module', '=', self.name),
                ('model', '=', 'ir.model.data')
            ]
            m_data_obj = self.env['ir.model.data']
            m_data_set = m_data_obj.search(m_data_domain)

            ids = [record.res_id for record in m_data_set]

            model_obj = self.env['ir.model']
            model_set = model_obj.browse(ids)

            for model in model_set:
                model = self.env['dev.code.tester']
                init_module_models(self.env.cr, 'development_tools', model)

        except Exception as ex:
            _logger.error('compile %s' % ex)

    def _backup(self, source, target=None, restore=False):
        # STEP 1: File path must exists and it must be a file
        # STEP 2: Remove old backup file if exists
        # STEP 3: backup pyc file

        if not target:
            target = source + u'.bak'

        if restore:
            src_file = target
            dest_file = source
        else:
            src_file = source
            dest_file = target

        assert path.isfile(src_file), \
            _(u'{} is not a valid file')

        if path.isfile(dest_file):
            remove(dest_file)

        copy2(src_file, dest_file)

        return dest_file

    # -------------------------- AUXILIARY METHODS ----------------------------

    def _get_resource_paths(self, filter_fn=None):
        """ Get full path of each one of the resources (files) in module

            :filter (function): filter function `fn(parents, name, contents)`
            :return: list with full resource paths
        """

        paths = []

        tree = get_module_filetree(self.name, dir='.')
        pyc_args_list = self._get_paths_args(tree, filter_fn)

        for pyc_args in pyc_args_list:
            rel_path = dir_sep.join(pyc_args)
            full_path = get_module_resource(self.name, rel_path)

            paths.append(full_path)

        return paths

    def _get_paths_args(self, root, filter_fn=None, parents=None):
        """ Gets path parts each one of the resources in nested dictionaries

            :param root (dict): nested dictionaries from `get_module_filetree`
            :filter (function): filter function `fn(parents, name, contents)`
            :parents: reserved for recursion
            :return: list [[parent, child, ...], [parent, child, ...]]
        """
        paths = []
        parents = parents or []

        for key, value in root.iteritems():
            path = parents + [key]
            if type(value) == dict:
                paths += self._get_paths_args(value, filter_fn, path, )
            elif filter_fn:
                if filter_fn(parents, key, value):
                    paths.append(path)
            else:
                paths.append(path)

        return paths

    # ---------------------------- LOG MESSAGES -------------------------------

    def log(self, level, message, *args, **kwargs):
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
        'backing_up': _(u'Backing up \'{}\' current module build'),
        'backing_done': _(u'Backing up \'{}\' done.'),
        'compiling': _(u'Compiling \'{}\'...'),
        'compilation_done': _(u'\'{}\' compilation has been completed.'),
        'compilation_fail': _(u'\'{}\' compilation has fail, restoring...'),
        'restoring_done': _(u'Previous state for \'{}\' has been restored.'),
        'compilation_proccess_fail': _(u'Compilation proccess fail <===')
    }

