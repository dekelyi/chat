#!/usr/bin/env python2
# coding=utf-8
"""
Client application
"""
import socket
from select import select
from sys import stdout, stdin
from os import name as os
import utils
import config

# platform specific implementaions
if os == 'nt':
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
        if os != 'nt':
            self.old_settings = termios.tcgetattr(stdin)
            tty.setcbreak(stdin.fileno())
            return self

    def __exit__(self, _type, value, traceback):
        if os != 'nt':
            termios.tcsetattr(stdin, termios.TCSADRAIN, self.old_settings)

    @staticmethod
    def has():
        """
        :rtype: bool
        :return: if there is new char input
        """
        if os == 'nt':
            return msvcrt.kbhit()
        return bool(select((stdin,), (), (), 0)[0])

    @staticmethod
    def get():
        """
        :rtype: str
        :return: char input, blocking
        """
        if os == 'nt':
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


class AsyncClient(object):
    """
    async chat-like client
    .. to be inherited

    :type _socket: socket.socket
    :type addr: tuple[str, int]
    """

    def __init__(self, address, port):
        """
        :type address: str
        :type port: int
        """
        self.addr = (address, port)
        self._socket = socket.socket()
        self._socket.connect(self.addr)
        self.on_init()

    def on_init(self):
        """
        additional things to do in the initialize of the client
        .. to be overridden
        """
        pass

    def on_data(self, _data):
        """
        process data sent by the server
        .. to be overridden

        :type _data: str
        :rtype: bool
        :return: to rewrite input or not
        :raise: Exception to signal EXIT
        """
        # split to messages
        _data = (utils.parse_msg(d) for d in _data.split('\n') if d)
        # separate control messages from data messages
        msgs = (d for d in _data if d['type'] == 'msg')
        # overwrite line
        stdout.write('\r')
        stdout.flush()
        # print messages
        for msg in msgs:
            print 'HIM:', msg['msg']
        return bool(_data)

    def main(self):
        """
        main processing of the client
        """
        try:
            with Reader() as reader:
                while True:
                    reader.get_data()
                    if reader.data[-1] == '\n' if reader.data else False:
                        # send message
                        if select((), (self._socket,), (), 0)[1]:
                            self._socket.send(utils.format_msg('msg', msg=reader.data[:-1]))
                        stdout.write('\r')
                        stdout.flush()
                        print 'YOU:', reader.data,
                        reader.data = ''
                    # else:
                    #     stdout.write('\r')
                    #     stdout.flush()
                    if select((self._socket,), (), (), 0)[0]:
                        _data = self._socket.recv(1024)  # type: str
                        _data = self.on_data(_data)
                        # rewrite input
                        if _data and reader.data:
                            stdout.write(reader.data)
                            stdout.flush()
        except socket.error:
            self._socket.close()
            print 'Error occurred, disconnected.'
        except KeyboardInterrupt:
            self._socket.close()


def main():
    """
    client demo
    """
    _client = AsyncClient(config.ADDRESS, config.PORT)
    _client.main()


if __name__ == '__main__':
    main()
