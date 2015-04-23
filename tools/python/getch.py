import sys
import colorama
import re

class Getch(object):
    """Gets a single character from standard input.  Does not echo to the
        screen.

    """

    def __init__(self):
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()

    def __call__(self): return self.impl()


class GetchUnix(object):
    def __init__(self):
        import tty, sys

    def __call__(self):
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class GetchWindows(object):
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


class Keyboard(object):

    getch = Getch()

    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    RESET = '\033[0;0m'
    BOLD = '\033[1m'
    REVERSE = '\033[2m'

    BLACKBG = '\033[40m'
    REDBG = '\033[41m'
    GREENBG = '\033[42m'
    YELLOWBG = '\033[43m'
    BLUEBG = '\033[44m'
    MAGENTABG = '\033[45m'
    CYANBG = '\033[46m'
    WHITEBG = '\033[47m'

    def move(self, new_x, new_y):
        'Move cursor to new_x, new_y'
        sys.stdout.write('\033[' + str(new_y) + ';' + str(new_x) + 'H')

    def moveUp(self, lines):
        'Move cursor up # of lines'
        sys.stdout.write('\033[' + str(lines) + 'A')

    def moveDown(self, lines):
        'Move cursor down # of lines'
        sys.stdout.write('\033[' + str(lines) + 'B')

    def moveForward(self, chars):
        'Move cursor forward # of chars'
        sys.stdout.write('\033[' + str(chars) + 'C')

    def moveBack(self, chars):
        'Move cursor backward # of chars'
        sys.stdout.write('\033[' + str(chars) + 'D')

    def save(self):
        'Saves cursor position'
        sys.stdout.write('\033[s')

    def restore(self):
        'Restores cursor position'
        sys.stdout.write('\033[u')

    def clear(self):
        'Clears screen and homes cursor'
        sys.stdout.write('\033[2J')

    def clrtoeol(self):
        'Clears screen to end of line'
        sys.stdout.write('\033[K')

    def blink(self, on=True):
        sys.stdout.write('\033[?25h' if on else '\033[?25l')

    def _textbox_area(self, x, y, length):
        self.move(x, y)
        for cx in range(0, length + 2):
            sys.stdout.write(' ')

    def textbox(self, x, y, length, allowed=r'[\x20-\xFE]'):
        k = False
        ctrl = False

        regex = re.compile(allowed)

        cx = 1

        sys.stdout.write(self.WHITEBG + self.BLACK)
        self._textbox_area(x, y, length)
        self.move(x + 1, y)

        while not k or ord(k) != 27:
            ctrl, k = None, self.getch()
            if ord(k) in [224, 0]:
                ctrl = k
                k = self.getch()
            else:
                if ctrl and ord(ctrl) == 224:
                    if cx <= length and ord(k) == 77:
                        self.moveForward(1)
                        cx += 1
                    elif cx > 1 and ord(k) == 75:
                        self.moveBack(1)
                        cx -= 1
                elif cx > 1 and ord(k) == 8:
                    self.moveBack(1)
                    sys.stdout.write(' ')
                    self.moveBack(1)
                    cx -= 1
                elif cx <= length and regex.match(k):
                    cx += 1
                    sys.stdout.write(k)

    def options(self, x, y, _in_opt = ['True', 'False']):
        options = []

        self.move(x, y)
        px = x
        k = False
        index = 0

        for opt in _in_opt:
            option = {
                'text': ' {} '.format(opt),
                'position': px,
            }

            self.move(px, y)
            sys.stdout.write(option['text'])

            options.append(option)
            px += len(option['text']) + 1

        _max = len(options) - 1
        while not k or ord(k) != 13:
            k = self.getch()

            if ord(k) == 9:
                if index < _max:
                    index += 1
                else:
                    index = 0

                for idx, opt in enumerate(options):
                    self.move(opt['position'], y)
                    if idx == index:
                        sys.stdout.write(self.WHITEBG + self.BLACK)

                    sys.stdout.write(opt['text'])
                    sys.stdout.write(self.RESET)



    def __init__(self):
        colorama.init()
        self.save()

    def __del__(self):
        sys.stdout.write(self.RESET)
        self.restore()

# You have pressed: 72 224
# You have pressed: 77 224
# You have pressed: 80 224
# You have pressed: 75 224

#Keyboard().textbox(5, 2, 10)
Keyboard().options(5, 5)
