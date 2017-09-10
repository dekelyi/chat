#!/usr/bin/env python2
# coding=utf-8
"""
Async conosle reader class
"""
import os
from select import select
from sys import stdout, stdin

# platform specific implementaions
if os.name == 'nt':
    import msvcrt  # pylint: disable=import-error
else:
    import termios  # pylint: disable=import-error
    import tty  # pylint: disable=import-error


class Reader(object):
    """
    handles non-blocking async input on console
    needs to be used as a context manager (`with` statement) on linux.
    can word without in Windows

    :type data: str
    :type last: str
    """
    def __init__(self):
        self.data = ''
        self.last = ''
        self.old_settings = None

    def __enter__(self):
        if os.name != 'nt':
            self.old_settings = termios.tcgetattr(stdin)
            tty.setcbreak(stdin.fileno())
            return self

    def __exit__(self, _type, value, traceback):
        if os.name != 'nt':
            termios.tcsetattr(stdin, termios.TCSADRAIN, self.old_settings)

    @staticmethod
    def has():
        """
        :rtype: bool
        :return: if there is new char input
        """
        if os.name == 'nt':
            return msvcrt.kbhit()
        return bool(select((stdin,), (), (), 0)[0])

    @staticmethod
    def get():
        """
        :rtype: str
        :return: char input, blocking
        """
        if os.name == 'nt':
            return msvcrt.getch().decode('utf-8')
        return stdin.read(1)

    def get_has(self):
        """
        :rtype: str
        :return: char input, if any
        """
        if self.has():
            return self.get()
        return ''

    def show(self):
        """
        process char input and return

        :rtype: str
        :return: char input
        """
        self.last = string = self.get()
        self.data += string
        if string:
            if string == '\n':
                pass
            elif string == '\x7f':
                # backspace
                self.data = self.data[:-2] if len(self.data) > 2 else ''
                stdout.write('\r' + self.data + ' ' + '\r' + self.data)
                stdout.flush()
            else:
                stdout.write(string)
                stdout.flush()
        return string

    def get_data(self):
        """
        process all recent input

        :rtype: str
        :return: input
        """
        while self.has():
            self.show()
        return self.data.strip()

    def read_line(self):
        """
        Blocking line reading from stdout
        """
        while True:
            data = self.get_data()
            if self.data.endswith('\n'):
                self.data = ''
                return data
