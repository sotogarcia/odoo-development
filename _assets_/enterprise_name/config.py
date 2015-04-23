# -*- coding: utf-8 -*-

from os import path
import sys
import getopt
import logging
import xml.etree.ElementTree as ElementTree


class EventHook(object):
    # http://www.voidspace.org.uk/python/weblog/arch_d7_2007_02_03.shtml#e616

    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler


class Event(object):
    pass


class VerboseEvent(Event):
    message = None

    def __init__(self, message):
        self.message = self._format(message)

    def _format(self, message):
        return u'{}'.format(message)

class ErrorEvent(VerboseEvent):
    def _format(self, message):
        return u'OPS! {}'.format(message)


class PartnerModel(object):

    def __init__(self):
        self.name = None
        self.company_id = None
        self.image = None
        self.customer = None
        self.supplier = None
        self.is_company = None
        self.street = None
        self.street2 = None
        self.city = None
        self.zip = None
        self.country_id = None
        self.phone = None
        self.mobile = None
        self.email = None
        self.website = None
        self.lang = None

class EnterpriseSettingsApp (object):

    def show_help(self):
        print('show_help')
        f = path.basename(sys.argv[0])
        m = '\n\t* Use: {} [--name=regex] [--path=regex] [--help]'.format(f)
        print(m)

    def _proccess_command_line_arguments(self):
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], 'hv:', ['help', 'verbose'])

            for o, a in opts:
                if o in ('h', '--help'):
                    self.show_help()
                elif o in ('v', '--verbose'):
                    self.verbose = True
                else:
                    assert False, 'unhandled option'

        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

    def _print_message(self, event):
        if self.verbose:
            print(event.message)

    def _verbose(self, msg, *args, **kwargs):
        message = msg.format(*args, **kwargs)
        event = VerboseEvent(message)
        self.onVerbose.fire(event)

    def _get_file_path(self, item_folder, filename):
        return u'{}/{}.xml'.format(item_folder, filename)

    def _xml_file_exists(self, filepath):
        found = path.isfile(filepath)

        self._verbose(u'File {} has been found: {}', filepath, found)

        return found

    def _xml_read_file(self, filepath):
        tree = False

        try:
            assert self._xml_file_exists(filepath), \
                u'File {} does not exists'.format(filepath)
            tree = ElementTree.parse(filepath)
            self._verbose(
                u'File {} has been read: {}', filepath, bool(tree)
            )
        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

        return tree

    def _xml_get_records(self, xmltree, record_id=False):
        xpath = './/record'
        records = []

        if record_id:
            xpath += '[@id="{}"]'.format(record_id)

        try:
            root = xmltree.getroot()
            records = root.findall(xpath)
            self._verbose(u'Records loaded: {}', len(records))
        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

        return records

    def _is_attribute(self, model, child):
        is_field = (child.tag == 'field')
        has_name = 'name' in child.attrib
        is_valid = has_name and hasattr(model, child.attrib['name'])

        return is_field and has_name and is_valid

    def _get_name(self, child):
        name = False

        if 'name' in child.attrib:
            name = child.attrib['name']

        return name

    def _get_value(self, child):
        value = False

        if child.text:
            value = child.text
        elif u'eval' in child.attrib:
            value = child.attrib[u'eval']
        elif u'ref' in child.attrib:
            value = child.attrib[u'ref']

        return value

    def _create_model(self, record):
        model = PartnerModel()

        #self._verbose(u'New instance of {}', type(model).__name__)

        for child in record:
            if self._is_attribute(model, child):
                name = self._get_name(child)
                value = self._get_value(child)

                if name and value:
                    #self._verbose(u'    {:10}: {}', name, value)
                    setattr(model, name, value)

        return model

    def __init__(self):
        self.onError = EventHook()
        self.onError += self._print_message

        self.onVerbose = EventHook()
        self.onVerbose += self._print_message
        self.verbose = False

        self._proccess_command_line_arguments()

        path = self._get_file_path('data', 'res_partner')

        tree = self._xml_read_file(path)
        if tree:
            records = self._xml_get_records(tree) #, 'base.partner_root')

            for record in records:
                self._create_model(record)

EnterpriseSettingsApp()
