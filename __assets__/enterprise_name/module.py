# -*- coding: utf-8 -*-

from os import path
import abc
import sys
import getopt
import xml.etree.ElementTree as ElementTree
import re


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


class BaseClass(object):

    """ Base class to be extended by all in this module """

    onVerbose = EventHook()

    def __init__(self):
        pass

    def _debug(self, msg, *args, **kwargs):
        event = VerboseEvent(3, msg, *args, **kwargs)
        self.onVerbose.fire(event)

    def _info(self, msg, *args, **kwargs):
        event = VerboseEvent(2, msg, *args, **kwargs)
        self.onVerbose.fire(event)

    def _warn(self, msg, *args, **kwargs):
        event = VerboseEvent(1, msg, *args, **kwargs)
        self.onVerbose.fire(event)

    def _error(self, msg, *args, **kwargs):
        event = VerboseEvent(0, msg, *args, **kwargs)
        self.onVerbose.fire(event)


class ModuleApp(BaseClass):
    """ Application """

    def __init__(self):
        BaseClass.__init__(self)

        XMLRecordSet.onVerbose += self._print_messages

        self.partners = XMLRecordSet('data/res_partner.xml')
        self.users = XMLRecordSet('data/res_users.xml')
        self.companies = XMLRecordSet('data/res_company.xml')

        self.partners.parse()
        self.users.parse()
        self.companies.parse()

    def _print_messages(self, event):
        levels = ['ERROR', 'WARNING', 'INFO', 'DEBUG']

        if event.level < 3:
            print(u'{:7}: {}'.format(levels[event.level], event.message))


class XMLRecordSet(BaseClass):
    """Proccess all record tags in one XML file"""

    def __init__(self, filepath):
        BaseClass.__init__(self)
        self.filepath = filepath

    def parse(self):
        records = []

        tree = self._xml_read_file(self.filepath)
        if tree:
            records = self._xml_get_records(tree)
        else:
            self._warn(u'File {} is not readable', self.filepath)

        self._info(u'{} records in {}', len(records), self.filepath)

        for record in records:
            new = self._instance_model(record)

            for child in record:
                if self._is_attribute(new, child):
                    name = self._get_name(child)
                    value = self._get_value_str(child)

                    if name and value:
                        self._debug(u'\t{}: {}', name, value)
                        setattr(new, name, value)
                else:
                    self._warn(u'Invalid attribute for {}', type(new))

    def _instance_model(self, record):
        instance = False

        try:
            model_name = self._get_model_name(record)
            model_obj = eval(model_name)
            instance = model_obj()
            self._debug(u'New instance of {} has been created', model_name)
        except Exception as ex:
            self._error(ex.message)

        return instance

    def _get_model_name(self, record):
        name = False

        if 'model' in record.attrib:
            name = record.attrib['model']
            name = re.sub(r'(^|\.)(.)', lambda x: x.group(2).upper(), name)

        return name

    def _xml_file_exists(self, filepath):
        """ Check if file exists

            @param filepath (string): file path to be checked
            @return (bool): True if the file exists or False otherwise

        """

        found = path.isfile(filepath)
        self._info(u'File {} has been found: {}', filepath, found)

        return found

    def _xml_read_file(self, filepath):
        """ Read an XML file

            @param filepath (string): file path to be read
            @return (ElementTree/bool): XML tree if success else False

        """
        tree = False

        try:
            assert self._xml_file_exists(filepath), \
                u'File {} does not exists'.format(filepath)
            tree = ElementTree.parse(filepath)
            self._info(u'File {} has been read: {}', filepath, bool(tree))
        except Exception as ex:
            self._error(ex.message)

        return tree

    def _xml_get_records(self, xmltree, record_id=False):
        """ Find all <record> tags in XML and return them as XML elements

            @param xmltree (ElementTree): XML tree returned by _xml_read_file
            @record_id (string): id of the record to be retrieve or False to
            retrieve all.

            @return (list): list with all XML <record> elements

        """
        xpath = './/record'
        records = []

        if record_id:
            xpath += '[@id="{}"]'.format(record_id)

        try:
            root = xmltree.getroot()
            records = root.findall(xpath)
            self._info(u'Records loaded: {}', len(records))
        except Exception as ex:
            self._error(ex.message)

        return records

    def _is_attribute(self, model, child):
        """ Check if an XML field tag is a valid model attribute

            @param model (class): Model which has the valid fields
            @param child (ElementTree): XML field tag to be checked

            @return (bool): True if is a valid field or False otherwise.

        """
        is_field = (child.tag == 'field')
        has_name = 'name' in child.attrib
        is_valid = has_name and hasattr(model, child.attrib['name'])

        return is_field and has_name and is_valid

    def _get_name(self, child):
        """ Get the value of the 'name' attribute of XML field tag

             @param child (ElementTree): XML field tag which has the 'name'

             @return (string/bool): value of the name attrib if exists or False
        """

        name = False

        if 'name' in child.attrib:
            name = child.attrib['name']

        return name

    def _get_value_str(self, child):
        """ Get the value of an XML field tag. This value can be, in order,
            the text of the tag, an 'eval' attribute or a 'ref' attribute.

            @param child (ElementTree): XML field tag which has the value

            @return (string/bool): value of the name attrib if exists or False
        """

        value = False

        if child.text:
            value = child.text
        elif u'eval' in child.attrib:
            value = child.attrib[u'eval']
        elif u'ref' in child.attrib:
            value = child.attrib[u'ref']

        return value


class Event(object):

    """ Abstract Generic Event Class """

    __metaclass__ = abc.ABCMeta


class VerboseEvent(Event):

    """ Class which stores messages from application """

    def __init__(self, level, msg, *args, **kwargs):
        self.level = level
        self.message = msg.format(*args, **kwargs)


class ResPartner(object):

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
        self.commercial_partner_id = None
        self.parent_id = None
        self.function = None
        self.use_parent_address = None

class ResUsers(object):

    def __init__(self):
        self.name = None
        self.login = None
        self.partner_id = None
        self.lang = None
        self.tz = None
        self.action_id = None
        self.signature = None
        self.password = None

class ResCompany(object):

    def __init__(self):
        self.name = None
        self.name = None
        self.partner_id = None
        self.currency_id = None
        self.rml_paper_format = None
        self.paperformat_id = None
        self.rml_header1 = None
        self.rml_header2 = None
        self.rml_header3 = None
        self.rml_footer = None
        self.custom_footer = None
        self.logo_web = None
        self.font = None
        self.account_no = None
        self.email = None
        self.phone = None
        self.fax = None
        self.company_registry = None

ModuleApp()

