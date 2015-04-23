# -*- coding: utf-8 -*-
import sys
import colorama
import re
import abc
from time import sleep



# --------------------------------- CONTROLS ---------------------------------


class Control(object):
    """ Controls abstract base class

        Attibutes:
          - x  (int): horizontal left position in characters
          - y  (int): vertical top position in lines
          - cx (int): width of the client área in characters
          - cy (int): height of the client área in characters

        Evetns:
          - onFocus (FocusEvent): Event triggered when control gets focus
          - onError (ErrorEvent): Event triggered when error occurs
          - onKeyPress (KeypressEvent): Event triggered when key is pressed

    """
    __metaclass__ = abc.ABCMeta

    onError = None  # The same error behavior for all the controls
    onFocus = None  # The same focus behavior for all the controls

    def __init__(self, name, **kwargs):
        self.name = name

        self._kbrd = Keyboard()

        self._transparent = kwargs.get('transparent', False)

        brush = kwargs.get('brush', 'WHITEBG')
        self._brush = getattr(self._kbrd, brush)

        pen = kwargs.get('pen', 'BLACK')
        self._pen = getattr(self._kbrd, pen)

        self._x = kwargs.get('x', 1)
        self._y = kwargs.get('y', 1)

        self._width = kwargs.get('cx', 3)
        self._height = kwargs.get('cy', 1)

        self.onError = EventHook()
        self.onFocus = EventHook()
        self.onKeyPress = EventHook()

    def _error(self, msg_format, *args, **kwargs):
        msg = msg_format.format(*args, **kwargs)
        error_event = ErrorEvent(msg)
        self.onError.fire(error_event)

    def _begin_paint(self, erase=True):
        paint = sys.stdout.write
        kbrd = self._kbrd

        if not self._transparent:
            paint(self._brush + self._pen)

        if erase:
            for cx in range(0, self._width + 2):
                for cy in range(0, self._height):
                    kbrd.move(self._x + cx, self._y + cy)
                    paint(' ')

        return paint, kbrd

    def _end_paint(self, kbrd):
        sys.stdout.write(kbrd.RESET)

    def _invert_colors(self, update=True):
        old_pen = self._pen
        old_brush = self._brush

        self._pen = old_brush.__str__().replace('[4', '[3')
        self._brush = old_pen.__str__().replace('[3', '[4')

        if update:
            self.update()

    @abc.abstractmethod
    def update(self):
        return

    def focus(self):
        self._kbrd.move(self._x + 1, self._y)
        self.onFocus.fire(FocusEvent(self))

    def show(self):
        self.update()
        self.focus()

    def keypress(self, key):
        self.onKeyPress.fire(KeyPressEvent(key))


class TextBox(Control):
    """ Textbox control

        Attibutes:
          - obfuscate: hides charactes in texbox shown asterisks instead
          - text: default text value for textbox
          - allowed: regex pattern which determines allowed chars to be used

    """

    def __init__(self, name, **kwargs):
        Control.__init__(self, name, **kwargs)
        self._index = 0
        self._undo = ''
        self._text = ''

        self.allowed(kwargs.get('allowed', r'[\x20-\xFE]'))
        self._obfuscate = bool(kwargs.get('obfuscate', False))
        self._update_text(kwargs.get('text', '')[:self._width])

        self._index = max(0, len(self._update_text())-1)
        self._update_index()

    def update(self):
        paint, kbrd = self._begin_paint()

        self._kbrd.move(self._x + 1, self._y)

        text = self._update_text()
        text = '*' * len(text) if self._obfuscate else text
        paint(text)

        self._end_paint(kbrd)

    def text(self, text=None):
        text = self._update_text(text)

        if text:
            self._undo = text

        self._update_index(+self._width)

        return text

    def allowed(self, allowed=None):
        if allowed or allowed == '':
            self._regex = re.compile(allowed)

        return self._regex

    def keypress(self, key):
        if key.ctrl == 224:
            if key.code == 77:      # Fordward
                self._update_index(1)
            elif key.code == 75:    # Back
                self._update_index(-1)
            elif key.code == 71:    # Home
                self._update_index(-self._width)
            elif key.code == 79:
                self._update_index(+self._width)
            elif key.code == 83:
                self._delete()
        elif key.code == 8:
            self._backspace()
        elif key.code == 27:
            self.undo()
        else:
            if self._regex.match(key.char):
                self._write_char(key.char)

    def undo(self):
        self.text(self._undo)  # Update text and position

    def show(self):
        super(TextBox, self).show()
        self._update_index(+self._width)

    def _update_text(self, text=None):
        if text or text == '':

            if len(text) > self._width:
                self._error('Text is too long and will be truncated')

            text = text[:self._width]

            for char in list(text):
                if not self._regex.match(char):
                    self._error('Text not allowed')
                    text = ''
                    break

            self._text = text

            self._update_index()
            self.update()

        return self._text

    def _update_index(self, inc=0):

        l = len(self._update_text())    # One at right if it is not in the end
        w = self._width - 1     # Index base zero
        i = self._index + inc   # Wildly

        self._index = max(0, min(l, w, i))      # Prevent overflow

        self._kbrd.move(self._x + 1 + self._index, self._y)

    def _write_char(self, char):
        self._update_index()

        index = self._index
        chars = list(self._update_text() or '')
        length = len(chars)

        if length and index < length:
            chars[index] = char
        else:
            chars.append(char)

        self._update_text(''.join(chars))
        self._update_index(1)

    def _backspace(self):
        self._update_index()

        if self._index:
            if len(self._update_text()) == self._width:
                index = len(self._update_text()) - 1
            else:
                self._update_index(-1)
                index = self._index

            chars = list(self._update_text() or '')
            del(chars[index])
            self._update_text(''.join(chars))

    def _delete(self):
        chars = list(self._update_text() or '')
        length = len(chars)

        if length and self._index < length:
            del(chars[self._index])
            self._update_text(''.join(chars))


class Button(Control):

    def __init__(self, name, **kwargs):
        Control.__init__(self, name, **kwargs)

        self.onAction = EventHook()

        self.text(kwargs.get('text', 'OK'))
        self._cancel = kwargs.get('cancel', False)

    def text(self, text=None):
        if text:
            self._text = text[:self._width]

        return self._text

    def update(self):
        paint, kbrd = self._begin_paint()

        text = self.text()
        offset = (self._width - len(text)) // 2

        self._kbrd.move(self._x + offset + 1, self._y)
        paint(text)

        self._end_paint(kbrd)

    def focus(self):
        super(Button, self).focus()
        self._kbrd.move(self._x + 1 + self._width // 2, self._y)

    def keypress(self, key):
        if not key.ctrl:    # Prevent control keys
            if key.code in [32, 13]:
                self.onAction.fire(ActionEvent(key, 'accept'))
                self.actuate()
            elif key.code == 27 and self._cancel:
                self.onAction.fire(ActionEvent(key, 'cancel'))
                self.actuate()

    def actuate(self):
        old_pen = self._pen
        old_brush = self._brush

        self._pen = old_brush.__str__().replace('[4', '[3')
        self._brush = old_pen.__str__().replace('[3', '[4')
        self.update()

        sleep(0.05)

        self._pen = old_pen
        self._brush = old_brush
        self.update()


class OptionSet(Control):

    def __init__(self, name, **kwargs):
        Control.__init__(self, name, **kwargs)

        self._transparent = kwargs.get('transparent', True)

        self._options = []

        left = 0
        for text in kwargs.get('options', []):
            width = len(text)
            option = Button(
                text,
                x=self._x + left,
                y=self._y,
                cx=width,
                text=text,
                transparent=self._transparent
            )
            option.onError += self._on_child_error
            option.onKeyPress += self._on_child_key_press
            option.onFocus += self._on_child_focus

            self._options.append(option)
            left += width + 3

        self._index = 0 if self._options else -1

    def show(self):
        for option in self._options:
            option.show()

        self._options[self._index]._transparent = False
        self._options[self._index].show()

    def update(self):
        for option in self._options:
            option._transparent = self._transparent
            option.update()

        self._options[self._index]._transparent = False
        self._options[self._index].show()

    def index(self, index=None):
        return self._update_index(index, False)

    def keypress(self, key):
        if key.ctrl == 224 and self._options:
            if key.code == 77:      # Fordward
                self._update_index(1)
            elif key.code == 75:    # Back
                self._update_index(-1)
            elif key.code == 71:    # Home
                self._update_index(0, False)
            elif key.code == 79:
                self._update_index(len(self._options)-1, False)
            else:
                self._options[self._index].keypress(key)
        else:
            self._options[self._index].keypress(key)

        self.update()

    def _update_index(self, value, is_offset=True):
        _max = len(self._options) - 1
        _min = 0

        if _max > _min:

            if is_offset:
                self._index += value
            else:
                self._index = value

            if self._index > _max:
                self._index = _min
            elif self._index < _min:
                self._index = _max

    def _on_child_error(self, event):
        self.onError.fire(event)

    def _on_child_key_press(self, event):
        self.onKeyPress.fire(event)

    def _on_child_focus(self, event):
        # self.onFocus.fire(event)
        pass


class Caption(Control):

    def __init__(self, name, **kwargs):
        Control.__init__(self, name, **kwargs)
        self._text = ''

        text = self._update_text(kwargs.get('text', None))
        self._transparent = kwargs.get('transparent', True)

        self._width = kwargs.get('cx', len(self._text or self.name))

    def update(self):
        paint, kbrd = self._begin_paint()

        self._kbrd.move(self._x + 1, self._y)

        text = self._update_text()
        paint(text)

        self._end_paint(kbrd)

    def text(self, text=None):
        text = self._update_text(text)

        return text

    def _update_text(self, text=None):
        if text:
            self._text = text[:self._width]
            self.update()

        text = self._text or self.name
        return text[:self._width]


# ---------------------------------- EVENTS ----------------------------------


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
    """ Event abstrac base class """

    __metaclass__ = abc.ABCMeta


class ErrorEvent(Event):
    """ Store messages from error events """

    def __init__(self, message):
        self.message = message


class FocusEvent(Event):
    """ Store information about control which got focus """

    def __init__(self, ctrl):
        self.control = ctrl


class KeyPressEvent(Event):
    """ Store key information in keypress events """

    def __init__(self, key, used=False):
        self.key = key
        self.used = used

    def char(self):
        return self.key.char

    def code(self):
        return self.key.code

    def ctrl(self):
        return self.key.ctrl


class ActionEvent(KeyPressEvent):

    def __init__(self, key, action):
        self.key = key
        self.used = True
        self.action = action

# --------------------------------- KEYBOARD ---------------------------------


class Keyboard(object):
    """ Keyboard usefull methods and constants """

    _instance = None

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

    def __init__(self):
        colorama.init()
        self._getch = Getch()
        self.save()

    def __new__(cls, *args, **kargs):
        """ Singleton pattern http://es.wikipedia.org/wiki/Singleton#Python """

        if cls._instance is None:
            cls._instance = object.__new__(cls, *args, **kargs)

        return cls._instance

    def __del__(self):
        sys.stdout.write(self.RESET)
        self.restore()

    def getch(self, allowed=None):
        allowed = re.compile(allowed or r'.*')
        ctrl, key = None, None

        while not key:
            ctrl, k = None, self._getch()

            if ord(k) in [224, 0]:
                ctrl = k
                k = self._getch()

            if allowed.match(k):
                key = Key(k, ctrl)

        return key


class Key(object):
    """ Keyboard key data """

    def __init__(self, key, ctrl):
        self.char = key
        self.ctrl = ord(ctrl) if ctrl is not None else None
        self.code = ord(key)

    def __str__(self):
        msg = u'<{}.Key object {{\'ctrl\': {}, \'ord\': {}, \'char\': {}}}>'
        return msg.format(__name__, self.ctrl, self.code, self.char)


class Getch(object):
    """ Gets a single character from standard input.  Does not echo to the
        screen.

    """

    def __init__(self):
        try:
            self.impl = GetchWindows()
        except ImportError:
            self.impl = GetchUnix()

    def __call__(self): return self.impl()


class GetchUnix(object):
    """ Getch variant for unix systems """

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
    """ Getch variant for Windows systems """

    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()


# ---------------------------------- OTHER  ----------------------------------


class App(object):

    def __init__(self):
        self._kbrd = Keyboard()

        self._controls = []
        self._captions = []

        c1x1, c1x2 = 4, 12
        c2x1, c2x2 = 42, 50
        cap_cx, ctrl_cx = 6, 25
        y = 2

        options = [
            'Mister',
            'Miss',
        ]

        self._captions.append(Caption('Title', x=c1x1, y=y, cx=cap_cx))
        title = OptionSet('title', x=c1x2, y=y, options=options)
        self._controls.append(title)

        self._captions.append(Caption('Name', x=c2x1, y=y, cx=cap_cx))
        name = TextBox('name', x=c2x2, y=y, cx=ctrl_cx, text='Administrador')
        self._controls.append(name)
        y += 2

        self._captions.append(Caption('Street', x=c1x1, y=y, cx=cap_cx))
        street = TextBox('street', x=c1x2, y=y, cx=ctrl_cx)
        self._controls.append(street)

        self._captions.append(Caption('Stree2', x=c2x1, y=y, cx=cap_cx))
        street2 = TextBox('street2', x=c2x2, y=y, cx=ctrl_cx)
        self._controls.append(street2)
        y += 2

        self._captions.append(Caption('City', x=c1x1, y=y, cx=cap_cx))
        city = TextBox('city', x=c1x2, y=y, cx=ctrl_cx, text='Vigo')
        self._controls.append(city)

        self._captions.append(Caption('Zip', x=c2x1, y=y, cx=cap_cx))
        zip_code = TextBox('zip', x=c2x2, y=y, cx=5, text='36200')
        self._controls.append(zip_code)

        self._captions.append(Caption('State', x=c2x2 + 8, y=y, cx=5))
        state_id = TextBox('state_id', x=c2x2+15, y=y, cx=10)
        self._controls.append(state_id)
        y += 2

        self._captions.append(Caption('Phone', x=c1x1, y=y, cx=cap_cx))
        phone = TextBox('phone', x=c1x2, y=y, cx=ctrl_cx, text='+34 986 ')
        self._controls.append(phone)

        self._captions.append(Caption('Mobile', x=c2x1, y=y, cx=cap_cx))
        mobile = TextBox('mobile', x=c2x2, y=y, cx=ctrl_cx, text='+34 ')
        self._controls.append(mobile)
        y += 2

        self._captions.append(Caption('Fax', x=c1x1, y=y, cx=cap_cx))
        fax = TextBox('fax', x=c1x2, y=y, cx=ctrl_cx, text='+34 986 ')
        self._controls.append(fax)

        self._captions.append(Caption('Email', x=c2x1, y=y, cx=cap_cx))
        email = TextBox('email', x=c2x2, y=y, cx=ctrl_cx)
        self._controls.append(email)

        y += 4

        self._captions.append(Caption('Name', x=c1x1, y=y, cx=cap_cx))
        cname = TextBox('name', x=c1x2, y=y, cx=ctrl_cx)
        self._controls.append(cname)

        self._captions.append(Caption('Vat', x=c2x1, y=y, cx=cap_cx))
        cvat = TextBox('vat', x=c2x2, y=y, cx=ctrl_cx, text='+34 986 ')
        self._controls.append(cvat)
        y += 2

        self._captions.append(Caption('Header', x=c1x1, y=y, cx=cap_cx))
        cheader = TextBox('header', x=c1x2, y=y, cx=ctrl_cx)
        self._controls.append(cheader)

        self._captions.append(Caption('URL', x=c2x1, y=y, cx=cap_cx))
        curl = TextBox('url', x=c2x2, y=y, cx=ctrl_cx)
        self._controls.append(curl)
        y += 4

        self._captions.append(Caption('Module', x=c1x1, y=y, cx=cap_cx))
        module_name = TextBox('module', x=c1x2, y=y, cx=ctrl_cx)
        self._controls.append(module_name)

        cmd_save = Button('save', x=69, y=y, cx=6, text="Save")
        self._controls.append(cmd_save)

        cmd_reject = Button('reject', x=59, y=y, cx=6, text="Reject")
        self._controls.append(cmd_reject)

        self._index = 0

    def _update_index(self, offset):
        self._index += offset

        _max = len(self._controls) - 1
        _min = 0

        if self._index < _min:
            self._index = _max
        elif self._index > _max:
            self._index = _min

    def _show(self):
        self._kbrd.clear()

        for control in self._controls:
            control.show()

        for caption in self._captions:
            caption.show()

        if self._controls:
            self._controls[self._index].show()

    def run(self):
        self._show()

        key = False
        while not key or key.code != 13:
            key = self._kbrd.getch()
            if key.code == 9:
                self._update_index(1)
                self._controls[self._index].show()
            else:
                self._controls[self._index].keypress(key)

        self._kbrd.clear()


App().run()
