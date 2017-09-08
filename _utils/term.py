from sys import stdout
import colorama
from _terminalsize import get_terminal_size

TERMSIZE = get_terminal_size()
ESC = chr(27)


def ansi(seq):
    return ESC + '[' + seq


def write(text):
    stdout.write(text)
    stdout.flush()


def clearline():
    write(ansi('2K'))


def clear():
    write(ansi('2J'))


def save():
    """
    Saves cursor position
    """
    write(ansi('s'))


def restore():
    """
    Restores cursor position
    """
    write(ansi('u'))


def position(x=0, y=0):
    write(colorama.Cursor.POS(x, y))
