"""
main client program
"""
import socket
from select import select
import threading
import errno
import sys
import _socket  # pylint: disable=unused-import
from Queue import Queue
from contextlib import contextmanager

import utils
from _client.connection import Connection
from _utils import term


class MainConnection(object):
    """
    :type addr: tuple
    :type lock: threading.Lock
    :type _socket: _socket.socket
    :type queue: Queue
    :type exit: bool
    :type connection: list[tuple[Connection, Queue]]
    """
    def __init__(self, addr):
        """
        :type addr: tuple
        """
        self.addr = addr
        self.lock = threading.Lock()

        self.socket_ = socket.socket()
        self.socket_.connect(addr)

        self.queue = Queue()

        self.exit = False

        self.connections = []

    def add_connection(self, kls):
        """
        adds a connection handler
        :param type kls: subclass of Connection
        """
        conn = kls(self)
        self.connections.append(conn)

    def on_data(self, data):
        """
        Send the data that arrived to all child connection excpet the sender

        :type data: basestring
        """
        if data == 'EXIT':
            raise SystemExit
        with self.lock:
            self.queue.put(data)

    def main(self):
        """
        main program loop
        """
        term.colorama.init()
        term.clear()
        for thread in self.connections:  # type: Connection
            thread.start()
        try:
            lst = (self.socket_,)
            while True:
                if self.exit:
                    raise KeyboardInterrupt
                with self.lock:
                    rlist, _, _ = select(lst, [], [], 0)
                    rlist = [(sock, sock.recv(1024)) for sock in rlist]
                for _, data in rlist:  # type: _socket.socket, basestring
                    if data == '':
                        raise KeyboardInterrupt
                    self.on_data(utils.parse_msg(data))
        except (KeyboardInterrupt, SystemExit):
            for thread in self.connections:  # type: Connection
                thread.kill()
            term.clear()
            term.position()
            self.socket_.close()
            sys.exit(1)
