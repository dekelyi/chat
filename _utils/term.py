"""
Utils for terminal control
"""
from sys import stdout
import colorama
from _terminalsize import get_terminal_size

TERMSIZE = get_terminal_size()
ESC = chr(27)


def ansi(seq):
    """
    Return ANSI sequence

    :param seq: ansi code
    """
    return ESC + '[' + seq


def write(text):
    """
    Write to stdout

    :param basestring text: text to write
    """
    stdout.write(text)
    stdout.flush()


def clearline():
    """
    Clear current line
    """
    write(ansi('2K'))


def clear():
    """
    Clear whole screen
    """
    write(ansi('2J'))


def save():
    """
    Save cursor position
    """
    write(ansi('s'))


def restore():
    """
    Restore cursor position
    """
    write(ansi('u'))


def position(x=0, y=0):
    """
    Change cursor position

    :param int x: x-axis
    :param int y: y-axis
    """
    write(colorama.Cursor.POS(x, y))


class PositionController(object):
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __call__(self, *args):
        text = ' '.join(args)
        print text
        self.y += 1

    def __enter__(self):
        save()
        position(self.x, self.y)
        return self

    def __exit__(self, *_):
        restore()
