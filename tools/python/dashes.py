# -*- coding: utf-8 -*-
from getopt import getopt, GetoptError
from sys import exit, argv
from os.path import basename

help_format = u"""
  Usage: {} --len=len --text=text --pre=pre --dash=dash --upper --help

    - len: length of the line including text and prefix (default: {}).
    - text: text to be added in the middle of the line (default: {}).
    - pre: text to be added in the begining of the line (default: {}).
    - dash: character will be used as dash (default: {}).
    - upper: convert given text to uppercase.
    - help: shows this help information.

  NOTE: all arguments are optional, to each one of the omitted item will be
  assigned to the default value.
"""

Hola


class Dashes(object):
    """ Singleton pattern, application class

        Attributes:

        _instance = saves the single possible instance of the class
    """

    _instance = None

    def __new__(cls, *args, **kargs):
        """ Code to manage the singleton pattern. This prevents the creation
            from more than one instance of this class.
        """

        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kargs)

        return cls._instance

    def __init__(self):
        """ Sets defaults, processes the command line and call the action """

        self._dash = '-'
        self._len = 75
        self._pre = '# '
        self._text = ''
        self._upper = False

        self._get_args()
        self._print_dashes()

    def _safe_int_parse(self, str, default):
        """ Tries to convert a given string into an integer and returns it or,
            if is not possible,  returns a default given value.

            :param str (str): string will be converted to integer
            :param default (int): integer will be used as returned value if the
            given string can not be converted.
            :return (int): integer value if the string could be converted or
            the default value otherwise.
        """

        result = default

        try:
            result = int(str)
        except Exception as ex:
            print ex

        return result

    def _get_args(self):
        """ Gets the arguments from command line and calls method which will
            process each of them.

            If it finds a unknown argument, shows help message and it exits
            returning a 2 as error code.
        """
        arg_list = ['help', 'len=', 'text=', 'pre=', 'test', 'upper']
        try:
            opts, args = getopt(argv[1:], "hltptdu:v", arg_list)
        except GetoptError:
            self._print_usage()
            exit(2)

        for opts, args in opts:
            self._proccess_args(opts, args)

    def _proccess_args(self, opts, args):
        """ Process each one of the arguments given in the command line

            :param opts (str): argument name with dashes and without equal sign
            :param args (args): argument value if applicable
        """

        if opts in ("-h", "--help"):
            self._print_usage()
            exit()
        elif opts in ("-l", "--len"):
            self._len = max(self._safe_int_parse(args, self._len), 10)
            self._update_pre()
            self._update_text()
        elif opts in ("-t", "--text"):
            self._update_text(args)
        elif opts in ("-p", "--pre"):
            self._update_pre(args)
        elif opts in ("-t", "--test"):
            self._test()
        elif opts in ("-d", "--dash"):
            self._dash = args[1:] if args else self._dash
        elif opts in ("-u", "--upper"):
            self._upper = True
            self._update_text()
        else:
            assert False, "unhandled option"

    def _update_text(self, new_text=False):
        """ Updates the text will be displayed, cutting it by the maximum
            allowed characters and it adds to it a space at the beginning and
            other at the end.

            :param new_text (bool): optional text will replace the existing
        """

        if new_text:
            self._text = new_text

        self._text = self._text.strip()[:self._len / 3]

        if self._text:
            self._text = ' %s ' % self._text

            if self._upper:
                self._text = self._text.upper()

    def _update_pre(self, new_text=False):
        """ Updates the prefix will be displayed, cutting it by the maximum
            allowed characters and it adds to it a space at the end.

            :param new_text (bool): optional prefix will replace the existing
        """

        if new_text:
            self._pre = new_text

        self._pre = self._pre.strip()[:self._len / 4]

        if self._pre:
            self._pre = '%s ' % self._pre

    def _print_usage(self):
        """ Prints the help information about how use this application """

        print help_format.format(
            basename(__file__),
            self._len,
            self._text,
            self._pre,
            self._dash
        )

    def _print_dashes(self):
        """ Prints the composited line by the prefix, the dashes and the text
            specified in the command line or the defaults instead.
        """

        ndashes = (self._len / 2) - (len(self._text) / 2)
        fit = int(self._len % 2)

        print '{}{}{}{}'.format(
            self._pre,
            self._dash * (ndashes - len(self._pre)),
            self._text,
            self._dash * (ndashes + fit),
        )[:self._len]

    def _test(self):
        """ Shows compositions with the extreme values.

            NOTE: this option is not mentioned in usage information.
        """
        self._print_dashes()
        self._proccess_args('--text', 'Hola')
        self._print_dashes()
        self._proccess_args('--text', 'Holas')
        self._print_dashes()

        self._proccess_args('--pre', '//////')

        self._print_dashes()
        self._proccess_args('--text', 'Hola')
        self._print_dashes()
        self._proccess_args('--text', 'Holas')
        self._print_dashes()

        self._proccess_args('--text', 'Perico de los palotes')
        self._proccess_args('--pre', '//////')
        self._proccess_args('--len', '1')
        self._print_dashes()

        exit(0)

Dashes()  # Program entry point
