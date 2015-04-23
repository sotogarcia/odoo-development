import os
import sys
import getopt
from re import compile as regex_compile, sub as regex_replace
import ctypes


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


class ErrorEvent(Event):
    message = None

    def __init__(cls, message):
        cls.message = message


class FoundEvent(Event):
    name = None
    path = None

    def __init__(cls, path, name):
        cls.name = name
        cls.path = path


class GetHelpEvent(Event):
    message = None

    def __init__(cls, message):
        cls.message = message


class LinkEvent(Event):
    source = None
    target = None
    directory = None

    def __init__(cls, source, target, directory):
        cls.source = source
        cls.target = target
        cls.directory = directory


class SymbolicLinks(object):
    onError = None
    onFound = None
    onGetHelp = None
    onLink = None

    regex_name = None
    regex_path = None

    show_help = False
    link_path = False

    def __init__(self):
        self.onError = EventHook()
        self.onFound = EventHook()
        self.onGetHelp = EventHook()
        self.onLink = EventHook()

    def _is_module(self, files):
        return '__openerp__.py' in files

    def _is_ported(self, root):
        return '__unported__' not in root.split('\\')

    def _list_modules(self):
        regex_path = regex_compile(self.regex_path or '.*')
        regex_name = regex_compile(self.regex_name or '.*')

        module_list = {}

        try:
            for root, dirs, files in os.walk("."):
                if self._is_module(files) and self._is_ported(root):
                    path = os.path.abspath(root)
                    name = os.path.basename(root)

                    if regex_path.match(path) and regex_name.match(name):
                        module_list[name] = path
                        self.onFound.fire(FoundEvent(path, name))

        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

        return module_list

    def _proccess_command_line_arguments(self):
        try:
            opts, args = getopt.getopt(
                sys.argv[1:], 'npl?:', ['name=', 'path=', 'link=', 'help'])

            for o, a in opts:
                if o in ('-n', '--name'):
                    self.regex_name = self._remove_quotes(a)
                elif o in ('-p', '--path'):
                    self.regex_path = self._remove_quotes(a)
                elif o in ('-l', '--link'):
                    self.link_path = self._remove_quotes(a)
                elif o in ('-?', '--help'):
                    self.show_help = True
                else:
                    assert False, 'unhandled option'

        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

    def _create_link(self, fileSrc, fileTarget, directory=1):
        try:
            kdll = ctypes.windll.LoadLibrary("kernel32.dll")
            kdll.CreateSymbolicLinkA(fileSrc, fileTarget, directory)
            self.onLink.fire(LinkEvent(fileSrc, fileTarget, directory))
        except Exception as ex:
            self.onError.fire(ErrorEvent(ex.message))

    def _remove_quotes(self, string):
        return regex_replace(r'^[\'"]?([^\'"]+)[\'"]?', r'\1', string)

    def get_help(self):
        f = os.path.basename(sys.argv[0])
        m = '\n\t* Use: {} [--name=regex] [--path=regex] [--help]'.format(f)
        self.onGetHelp.fire(GetHelpEvent(m))
        return m

    def run(self):
        self._proccess_command_line_arguments()

        if self.show_help:
            return self.get_help()
        else:
            module_list = self._list_modules()
            if module_list and self.link_path:
                for name, path in module_list.iteritems():
                    source = '{}\{}'.format(self.link_path, name)
                    self._create_link(source, path)


def onError(event):
    print(event.message)


def onFound(event):
    print('Found: {}'.format(event.name))


def onGetHelp(event):
    print(event.message)


def onLink(event):
    m = 'mklink {} {} {}'.format(
        '/d' if event.directory else '',
        event.source,
        event.target
    )
    print(m)

this = SymbolicLinks()

this.onError += onError
this.onFound += onFound
this.onGetHelp += onGetHelp
this.onLink += onLink

this.run()
