from compileall import compile_file, compile_dir
from os import path
from getopt import getopt, GetoptError
from sys import argv, exit


class App(object):

    """ Class with all script behavior inside

        Attributes:
          @path (string): path which contains files will be compiled.
          @force (bool): force compiled even if the timestamps are up to date.

    """

    def __init__(self):
        """ Class constructor, it sets the default values and invokes method
            which will process command line arguments.

            Later, it invokes needed methods to compile files according the
            command line options.

        """

        self.path = False
        self.force = False

        self._process_args()

        if not self.path:
            self.path = self._get_current_dir()

        self._start_info()
        self._compile()

    def _process_args(self):
        """ Process the command line getting values which will determine the
            script behavior. All process in inside try...except block.

        """

        try:
            optlist, args = getopt(
                argv[1:], ':fph:', ['force', 'path=', 'help'])

            for arg, value in optlist:
                if arg in ('-h', '--help'):
                    self._usage()
                    exit(0)
                elif arg in ('-f', '--force'):
                    self.force = True
                elif arg in ('-p', '--path'):
                    self.path = value
                else:
                    self._error(2, u'Invalid argument ({})', arg)

        except GetoptError as error:
            self._error(1, u'{}', error)

    def _get_current_dir(self):
        """ Get the current directory path

            @return (string): return full path

        """
        return path.dirname(path.abspath(__file__))

    def _compile(self):
        """ Launch the compilation process inside try...except block

        """

        try:
            assert path.exists(self.path), \
                u'Path {} is invalid'.format(self.path)

            if path.isdir(self.path):
                compile_dir(self.path, force=self.force)
            elif path.isfile(self.path):
                compile_file(self.path, force=self.force)
        except Exception as ex:
            self._error(3, u'{}', ex.message)

    def _start_info(self):
        """ Display values stored in variables which will determine the script
            behavior

        """
        app_path = path.basename(argv[0])
        msg = u'{} --path={} --force={}\n'
        self._print(False, msg, app_path, self.path, self.force)

    def _usage(self):
        """ Display command line help in console

        """
        app_path = path.basename(argv[0])
        msg = u'{} [--path=path] [--force] [--help]'
        self._print(u'USAGE', msg, app_path)

    def _error(self, code, msg, *args, **kwargs):
        """ Print error messages in console and exit script

            @param code (int): script exit code
            @param prefix (string): prefix to be added before message
            @param msg (string): message format

        """

        self._print(u'*ERROR', msg, *args, **kwargs)
        exit(code)

    def _print(self, prefix, msg, *args, **kwargs):
        """ Print messages in console

            @param prefix (string): prefix to be added before message
            @param msg (string): message format

        """

        if prefix:
            message = u'  {:6}: {}'.format(prefix[:6], msg)
        else:
            message = msg

        print (message.format(*args, **kwargs))

App()
